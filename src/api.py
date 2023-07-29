from flask import Blueprint, make_response, request, current_app, render_template, url_for, redirect
from flask_login import login_required
from jinja2_fragments.flask import render_block
from src.forms import link_form_builder, ClienteRegis, ProponenteForm
from src.models import Links, Cliente, Propostas, Telefone

api = Blueprint('api', __name__)


@api.post('/links/')
def gerar_link():
    form = link_form_builder('FIP FIM FIS FIE FIV PAM PAE PIEDU'.split())
    if not form.validate():
        resposta = make_response(render_template('htmx/link_form.html', form=form))
        resposta.headers['HX-Retarget'] = '#formProposta'
        return resposta
    cpf = form.cpf.data
    props = request.form.getlist('check')

    if cli := Cliente.query.filter_by(cpf=cpf).first():
        resposta = make_response()
        resposta.headers['HX-Redirect'] = url_for('views.pesquisar', cpf=cli.cpf)
        return resposta
    cliente = Cliente(cpf=cpf, nome=form.nome.data)
    current_app.db.session.add(cliente)
    current_app.db.session.commit()
    cliente = Cliente.query.filter_by(cpf=cpf).first()
    url = str(current_app.hashid.encode(cliente.id))
    link = Links(link=url)
    telefone = Telefone(telefone=form.telefone.data)
    cliente.links.append(link)
    cliente.telefones.append(telefone)
    for i in props:
        proposta = Propostas.query.filter_by(nome=i.upper()).first()
        cliente.links[0].propostas.append(proposta)
    current_app.db.session.commit()
    resposta = make_response(render_template('htmx/link_form.html', form=form, link=url_for('lead.oi', hashdd=url)))
    resposta.headers['HX-Retarget'] = '#formProposta'
    return resposta


@api.get('/permissoes/<id>')
@login_required
def permissoes(id):
    cliente = Cliente.query.get(id)
    form = link_form_builder('FIP FIM FIS FIE FIV PAM PAE PIEDU'.split(), **{prop.nome.upper(): True for prop in
                                                                             cliente.links[0].propostas})
    return render_template('htmx/form_permissoes.html', cliente=cliente, form=form)


@api.post('/editar/permissoes/<id>')
@login_required
def editar_permissoes(id):
    cliente = Cliente.query.get(id)
    alterar = request.form.getlist('check')
    props = [Propostas.query.filter_by(nome=nome).first() for nome in alterar]
    cliente.links[0].propostas = props
    current_app.db.session.commit()
    return render_block('cliente.html', 'ver_permissoes', cliente=cliente)


@api.post('/vip/logar')
def logar():
    form = ClienteRegis()
    if form.validate():
        cliente = Cliente.query.filter_by(cpf=form.cpf.data).first()
        cliente.senha = form.senha.data
        current_app.db.session.commit()
        return redirect(url_for('api.proponente'), code=307)
    return render_block('registrar.html', 'content', reg_form=form)


@api.post('/vip/proponente')
@login_required
def proponente():
    prop_form = ProponenteForm()
    return render_block('etapas.html', 'proponente', prop_form=prop_form)


def configure(app):
    app.register_blueprint(api, url_prefix='/api')
