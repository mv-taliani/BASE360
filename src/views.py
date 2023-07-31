import io

from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, send_file
from flask_login import login_required, current_user
import pdfkit
import flask_excel
import zipfile
from src.forms import link_form_builder
from src.models import Cliente, Preenchimento, Propostas, Detalhes, Links, Arquivos
from src.utils import get_s3

views = Blueprint('views', __name__)


@views.route('/')
@login_required
def index():
    return render_template('index.html')


@views.route('/vender')
@login_required
def vender():
    servicos = [x.nome for x in Propostas.query.all()]
    form = link_form_builder(servicos)
    return render_template('cadproposta.html', form=form)


@views.get('/cliente/<cpf>')
@login_required
def pesquisar(cpf):
    if current_user.hierarquia > 1:
        cliente = Cliente.query.filter_by(cpf=cpf).first()
        mensagem = 'Não encontrado'
    else:
        cliente = current_user.query.join(Cliente).filter_by(cpf=cpf).first()
        mensagem = 'Esse cliente pertence a outro vendendor'
    if not cliente:
        flash(mensagem, 'danger')
        return redirect(url_for('.vender'))
    return render_template('cliente.html', cliente=cliente)


@views.post('/cliente/')
@login_required
def pesquisar_post():
    dado = request.form.get('cpf').replace('.', '').replace('-', '').replace('(', '').replace(')', '')
    return redirect(url_for('.pesquisar', cpf=dado))


@views.get('/clientes')
@login_required
def clientes():
    if current_user.hierarquia > 1:
        cliente = Cliente.query.all()
    else:
        cliente = current_user.query.join(Cliente).all()
    if not cliente:
        flash('Você ainda não possui clientes!', 'primary')
        return redirect(url_for('views.vender'))
    return render_template('clientes.html', clientes=cliente)


@views.get('/cliente/arquivos/<cpf>/<proposta>')
def documentos(cpf, proposta):
    links = Arquivos.query.join(Preenchimento).join(Propostas).filter_by(nome=proposta).join(Links).join(Cliente).filter_by(cpf=cpf).all()
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for link in links:
            file_stream = get_s3(link.nome_aws)
            zip_file.writestr(link.nome_original, file_stream.getvalue())
    zip_buffer.seek(0)
    return send_file(zip_buffer, 'application/zip', True, f'{cpf}_{proposta}.zip')


@views.get('/cliente/tabela/<cpf>/<proposta>')
def tabela(cpf, proposta):
    preenchimento = Detalhes.query.join(Preenchimento).join(Propostas).filter_by(nome=proposta).join(Links).join(Cliente).filter_by(cpf=cpf).all()
    colunas = ['descricao', 'periodo', 'valor', 'justificativa']
    return flask_excel.make_response_from_query_sets(preenchimento, colunas, 'xlsx', file_name=f'{cpf}_{proposta}')


def configure(app):
    app.register_blueprint(views)
