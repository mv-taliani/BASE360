import decimal
import uuid
from itertools import groupby
import boto3
from flask import Blueprint, g, abort, render_template, current_app, redirect, url_for, flash, request, session
from flask_htmx import make_response
from jinja2_fragments.flask import render_block
from werkzeug.utils import secure_filename
from src.models import Propostas, Preenchimento, Detalhes, Links, Arquivos, Instituição, Recebimento
from src.forms import proponente_form, Etapa1Form, Etapa2Form, Etapa3Form, Etapa4Form, Etapa5Form, Etapa6Form, \
    Etapa7Form, Etapa8Form, DocumentoForm, EtapaFinalForm, RecebimentoForm, MESES
from src.utils import atualizar_preenchimento, upload_s3, somente_cliente, redirecionar_view, adicionar_etapa

oportunidades = Blueprint('oportunidades', __name__)


@oportunidades.url_value_preprocessor
def get_oportunidade(endpoint, values):
    oportunidade = values.pop('oportunidade')
    if oportunidade in [prop.nome for prop in g.cliente.links[0].propostas]:
        g.oportunidade = oportunidade
        session['oportunidade_id'] = next(filter(lambda x: x.nome == oportunidade, g.cliente.links[0].propostas)).id
        g.preenchimento = Preenchimento.query.join(Links).filter_by(link=g.cliente.links[0].link).join(
            Propostas).filter_by(nome=oportunidade).first()
        if not g.preenchimento:
            g.preenchimento = Preenchimento(link_id=g.cliente.links[0].id,
                                            proposta_id=next(filter(lambda x: x.nome == g.oportunidade,
                                                                    g.cliente.links[0].propostas)).id)
            current_app.db.session.add(g.preenchimento)
            current_app.db.session.commit()
    else:
        abort(404)


@oportunidades.route('/', methods=['GET', 'POST'])
@somente_cliente
def index():
    if g.oportunidade == 'FIM':
        return redirect(url_for('.etapa3', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade))
    prop_form = proponente_form(g.oportunidade)
    alvo = url_for('lead.oportunidades.index', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade)
    if current_app.htmx:
        if prop_form.validate():
            print(prop_form.data.items())
            atualizar_preenchimento(prop_form, g.preenchimento)
            current_app.db.session.commit()
            adicionar_etapa(link_id=session['link_id'], prop_id=session['oportunidade_id'], etapa='0 - Proponente')
            return make_response(
                redirect=url_for('.etapa1', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade))
        if request.method == 'GET':
            template = render_template('cadastro/proponente.html', prop_form=prop_form, alvo=alvo)
            return make_response(template, retarget='body', reswap='outerHTML')
        return render_block('cadastro/proponente.html', 'form', prop_form=prop_form, alvo=alvo)
    return render_template('cadastro/proponente.html', prop_form=prop_form, alvo=alvo)


@oportunidades.route('/etapa1', methods=['GET', 'POST'])
@somente_cliente
def etapa1():
    prop_form = Etapa1Form()
    alvo = url_for('lead.oportunidades.etapa1', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade)
    if current_app.htmx:
        if prop_form.validate():
            atualizar_preenchimento(prop_form, g.preenchimento)
            current_app.db.session.commit()
            adicionar_etapa(link_id=session['link_id'], prop_id=session['oportunidade_id'], etapa='1 - Identidade')
            return make_response(
                redirect=url_for('.etapa2', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade))
        if request.method == 'GET':
            template = render_template('cadastro/proponente.html', prop_form=prop_form, alvo=alvo)
            return make_response(template, retarget='body', reswap='outerHTML')
        return render_block('cadastro/proponente.html', 'form', prop_form=prop_form, alvo=alvo)
    return render_template('cadastro/proponente.html', prop_form=prop_form, alvo=alvo)


@oportunidades.route('/etapa2', methods=['GET', 'POST'])
@somente_cliente
def etapa2():
    prop_form = Etapa2Form()
    alvo = url_for('lead.oportunidades.etapa2', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade)
    if current_app.htmx:
        if prop_form.validate():
            atualizar_preenchimento(prop_form, g.preenchimento)
            current_app.db.session.commit()
            adicionar_etapa(link_id=session['link_id'], prop_id=session['oportunidade_id'],
                            etapa='2 - Análise do mercado')
            return make_response(
                redirect=url_for('.etapa3', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade))
        if request.method == 'GET':
            template = render_template('cadastro/proponente.html', prop_form=prop_form, alvo=alvo)
            return make_response(template, retarget='body', reswap='outerHTML')
        return render_block('cadastro/proponente.html', 'form', prop_form=prop_form, alvo=alvo)

    return render_template('cadastro/proponente.html', prop_form=prop_form, alvo=alvo)


@oportunidades.route('/etapa3', methods=['GET', 'POST'])
@somente_cliente
def etapa3():
    prop_form = Etapa3Form()
    alvo = url_for('lead.oportunidades.etapa3', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade)
    if current_app.htmx:
        if prop_form.validate():
            atualizar_preenchimento(prop_form, g.preenchimento)
            current_app.db.session.commit()
            adicionar_etapa(link_id=session['link_id'], prop_id=session['oportunidade_id'],
                            etapa='3 - Objetivos do Negócio')
            return make_response(
                redirect=url_for('.etapa4', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade))
        if request.method == 'GET':
            template = render_template('cadastro/proponente.html', prop_form=prop_form, alvo=alvo)
            return make_response(template, retarget='body', reswap='outerHTML')
        return render_block('cadastro/proponente.html', 'form', prop_form=prop_form, alvo=alvo)

    return render_template('cadastro/proponente.html', prop_form=prop_form, alvo=alvo)


@oportunidades.route('/etapa4', methods=['GET', 'POST'])
@somente_cliente
def etapa4():
    if g.oportunidade == 'FIM':
        return redirect(url_for('.etapa5', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade))
    prop_form = Etapa4Form()
    alvo = url_for('lead.oportunidades.etapa4', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade)
    if current_app.htmx:
        if prop_form.validate():
            atualizar_preenchimento(prop_form, g.preenchimento)
            current_app.db.session.commit()
            adicionar_etapa(link_id=session['link_id'], prop_id=session['oportunidade_id'], etapa='4 - Análise Swot')
            return make_response(
                redirect=url_for('.etapa5', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade))
        if request.method == 'GET':
            template = render_template('cadastro/proponente.html', prop_form=prop_form, alvo=alvo)
            return make_response(template, retarget='body', reswap='outerHTML')
        return render_block('cadastro/proponente.html', 'form', prop_form=prop_form, alvo=alvo)
    return render_template('cadastro/proponente.html', prop_form=prop_form, alvo=alvo)


@oportunidades.route('/etapa5', methods=['GET', 'POST'])
@somente_cliente
def etapa5():
    prop_form = Etapa5Form()
    alvo = url_for('lead.oportunidades.etapa5_add', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade)
    if [i for i in g.preenchimento.detalhes]:
        alvo2 = url_for('lead.oportunidades.etapa6', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade)
    else:
        alvo2 = None
    return render_template('cadastro/tabela.html', prop_form=prop_form, alvo=alvo, alvo2=alvo2)


@oportunidades.route('/etapa5_add', methods=['GET', 'POST'])
@somente_cliente
def etapa5_add():
    prop_form = Etapa5Form()
    alvo = url_for('lead.oportunidades.etapa5_add', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade)
    if current_app.htmx:
        if prop_form.validate():
            detalhe = Detalhes(**{key: value for key, value in prop_form.data.items()
                                  if key != 'csrf_token'})
            g.preenchimento.detalhes.append(detalhe)
            current_app.db.session.commit()
            adicionar_etapa(link_id=session['link_id'], prop_id=session['oportunidade_id'], etapa='5 - Tabela Detalhes')
            # if [i for i in g.preenchimento.detalhes]:
            #     alvo2 = url_for('lead.oportunidades.etapa6', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade)
            # else:
            #     alvo2 = None
            current_app.db.session.flush(detalhe)
            form = RecebimentoForm()
            template = render_template('cadastro/datas.html',
                                       total=sum([det.valor for det in g.preenchimento.detalhes]),
                                       form=form, id=detalhe.id)
            resposta = make_response(template, reswap='afterbegin')
            return resposta
        return render_block('cadastro/tabela.html', 'table', prop_form=prop_form, alvo=alvo)
    return render_block('cadastro/tabela.html', 'content', prop_form=prop_form, alvo=alvo)


@oportunidades.post('add_data/<id>')
@somente_cliente
def add_data(id):
    form = RecebimentoForm()
    detalhe = Detalhes.query.get(id)
    rcbmts = detalhe.recebimentos
    if form.validate():
        recebimento = Recebimento.query.filter_by(ano=form.ano.data, mes=form.mes.data).join(Detalhes).filter_by(id=id).first()
        if recebimento:
            total = sum([det.valor for det in g.preenchimento.detalhes]) - sum([rec.valor for rec in rcbmts])
            valor = decimal.Decimal(form.valor.data)
            if (soma := total - valor) < 0:
                form.valor.errors.append(f'Valor inválido! A diferença fica {soma}')
            else:
                recebimento.valor += valor
        else:
            recebimento = Recebimento(ano=form.ano.data, mes=form.mes.data, valor=form.valor.data)
            rcbmts.append(recebimento)
        current_app.db.session.commit()
    amv = [(i.ano, i.mes, i.valor) for i in rcbmts]
    anos = sorted(amv, key=lambda x: (x[0], MESES.index(x[1])))
    anos = groupby(anos, lambda x: x[0])

    total = sum([det.valor for det in g.preenchimento.detalhes]) - sum([rec.valor for rec in rcbmts])
    return render_template('cadastro/datas.html', id=id, rcbmts=rcbmts, anos=anos if anos else [], total=total,
                           form=form)


@oportunidades.route('/etapa6', methods=['GET', 'POST'])
@somente_cliente
def etapa6():
    if g.oportunidade == 'FIM':
        return make_response(redirect=url_for('.etapa9', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade))
    prop_form = Etapa6Form()
    alvo = url_for('lead.oportunidades.etapa6', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade)
    if current_app.htmx:
        if prop_form.validate():
            atualizar_preenchimento(prop_form, g.preenchimento)
            current_app.db.session.commit()
            adicionar_etapa(link_id=session['link_id'], prop_id=session['oportunidade_id'],
                            etapa='6 - Plano de Marketing')
            return make_response(
                redirect=url_for('.etapa7', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade))
        if request.method == 'GET':
            template = render_template('cadastro/proponente.html', prop_form=prop_form, alvo=alvo)
            return make_response(template, retarget='body', reswap='outerHTML')
        return render_block('cadastro/proponente.html', 'form', prop_form=prop_form, alvo=alvo)
    return render_template('cadastro/proponente.html', prop_form=prop_form, alvo=alvo)


@oportunidades.route('/etapa7', methods=['GET', 'POST'])
@somente_cliente
def etapa7():
    prop_form = Etapa7Form()
    alvo = url_for('lead.oportunidades.etapa7', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade)
    if current_app.htmx:
        if prop_form.validate():
            atualizar_preenchimento(prop_form, g.preenchimento)
            current_app.db.session.commit()
            adicionar_etapa(link_id=session['link_id'], prop_id=session['oportunidade_id'], etapa='7 - Planos Futuros')
            return make_response(
                redirect=url_for('.etapa8', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade))
        if request.method == 'GET':
            template = render_template('cadastro/proponente.html', prop_form=prop_form, alvo=alvo)
            return make_response(template, retarget='body', reswap='outerHTML')
        return render_block('cadastro/proponente.html', 'form', prop_form=prop_form, alvo=alvo)
    return render_template('cadastro/proponente.html', prop_form=prop_form, alvo=alvo)


@oportunidades.route('/etapa8', methods=['GET', 'POST'])
@somente_cliente
def etapa8():
    prop_form = Etapa8Form()
    alvo = url_for('lead.oportunidades.etapa8', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade)
    if current_app.htmx:
        if prop_form.validate():
            instituicao = Instituição()
            atualizar_preenchimento(prop_form, instituicao)
            g.preenchimento.insituicao.append(instituicao)
            current_app.db.session.commit()
            adicionar_etapa(link_id=session['link_id'], prop_id=session['oportunidade_id'],
                            etapa='8 - Contrapartida Social')
            return make_response(
                redirect=url_for('.etapa9', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade))
        flash("Nesta seção deverá ser preenchido a contrapartida social (Ou seja, dos 10% da verba destina ao CANS, 5% "
              "ficará para o CANS e os demais serão destinados a instituição descrita abaixo) -  Descreva a instituição",
              'primary')
        if request.method == 'GET':
            template = render_template('cadastro/proponente.html', prop_form=prop_form, alvo=alvo)
            return make_response(template, retarget='body', reswap='outerHTML')
        return render_block('cadastro/proponente.html', 'form', prop_form=prop_form, alvo=alvo)
    return render_template('cadastro/proponente.html', prop_form=prop_form, alvo=alvo)


@oportunidades.route('/etapa9', methods=['GET', 'POST'])
@somente_cliente
def etapa9():
    prop_form = DocumentoForm()
    alvo = url_for('lead.oportunidades.etapa9', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade)
    if current_app.htmx:
        if prop_form.validate_on_submit():
            # atualizar_preenchimento(prop_form, g.preenchimento)
            g.preenchimento.preenchido = True
            current_app.db.session.commit()
            for arquivo in prop_form.docs.data:
                pdf = Arquivos(nome_original=arquivo.filename)
                arquivo.filename = str(uuid.uuid4().hex) + f'{g.cliente.cpf}_{g.oportunidade}.pdf'
                pdf.nome_aws = arquivo.filename
                g.preenchimento.arquivos.append(pdf)
                current_app.db.session.commit()
                upload_s3(arquivo)
            adicionar_etapa(link_id=session['link_id'], prop_id=session['oportunidade_id'], etapa='9 - Arquivos')
            resposta = make_response(
                redirect=url_for('.etapafinal', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade))
            return resposta
        if request.method == 'GET':
            template = render_template('cadastro/proponente.html', prop_form=prop_form, alvo=alvo)
            return make_response(template, retarget='body', reswap='outerHTML')
        return render_block('cadastro/proponente.html', 'form', prop_form=prop_form, alvo=alvo)
    return render_template('cadastro/proponente.html', prop_form=prop_form, alvo=alvo)


@oportunidades.route('/etapafinal', methods=['GET', 'POST'])
@somente_cliente
def etapafinal():
    prop_form = EtapaFinalForm()
    alvo = url_for('lead.oportunidades.etapafinal', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade)
    if current_app.htmx:
        if prop_form.validate():
            atualizar_preenchimento(prop_form, g.preenchimento)
            current_app.db.session.commit()
            adicionar_etapa(link_id=session['link_id'], prop_id=session['oportunidade_id'], etapa='10 - Observações')
            return make_response(redirect=url_for('lead.oi', hashdd=g.cliente.links[0].link))
        if request.method == 'GET':
            template = render_template('cadastro/proponente.html', prop_form=prop_form, alvo=alvo)
            return make_response(template, retarget='body', reswap='outerHTML')
        return render_block('cadastro/proponente.html', 'form', prop_form=prop_form, alvo=alvo)
    return render_template('cadastro/proponente.html', prop_form=prop_form, alvo=alvo)


def configure(bp):
    bp.register_blueprint(oportunidades, url_prefix='/<oportunidade>')
