import boto3
from flask import Blueprint, g, abort, render_template, current_app, redirect, url_for, flash
from jinja2_fragments.flask import render_block
from werkzeug.utils import secure_filename
from src.models import Propostas, Preenchimento, Detalhes, Links
from src.forms import proponente_form, Etapa1Form, Etapa2Form, Etapa3Form, Etapa4Form, Etapa5Form, Etapa6Form, \
    Etapa7Form, Etapa8Form, DocumentoForm
from src.utils import atualizar_preenchimento, upload_s3

oportunidades = Blueprint('oportunidades', __name__)


@oportunidades.url_value_preprocessor
def get_oportunidade(endpoint, values):
    oportunidade = values.pop('oportunidade')
    if oportunidade in [prop.nome for prop in g.cliente.links[0].propostas]:
        g.oportunidade = oportunidade
        g.preenchimento = Preenchimento.query.join(Links).filter_by(link=g.cliente.links[0].link).join(Propostas).filter_by(nome=oportunidade).first()
    else:
        abort(404)


@oportunidades.route('/', methods=['GET', 'POST'])
def index():
    prop_form = proponente_form(g.oportunidade)
    alvo = url_for('lead.oportunidades.index', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade)
    if current_app.htmx:
        if prop_form.validate():
            preenchimento = Preenchimento(
                link_id=g.cliente.links[0].id,
                proposta_id=next(filter(lambda x: x.nome == g.oportunidade, g.cliente.links[0].propostas)).id)
            atualizar_preenchimento(prop_form, preenchimento)
            current_app.db.session.add(preenchimento)
            current_app.db.session.commit()
            return redirect(url_for('.etapa1', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade), code=307)
        return render_block('cadastro/proponente.html', 'content', prop_form=prop_form, alvo=alvo)
    return render_template('cadastro/proponente.html', prop_form=prop_form, alvo=alvo)


@oportunidades.post('/etapa1')
def etapa1():
    prop_form = Etapa1Form()
    alvo = url_for('lead.oportunidades.etapa1', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade)
    if current_app.htmx:
        if prop_form.validate():
            atualizar_preenchimento(prop_form, g.preenchimento)
            current_app.db.session.commit()
            return redirect(url_for('.etapa2', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade), code=307)
        return render_block('cadastro/proponente.html', 'content', prop_form=prop_form, alvo=alvo)

    return render_template('cadastro/proponente.html', prop_form=prop_form, alvo=alvo)


@oportunidades.post('/etapa2')
def etapa2():
    prop_form = Etapa2Form()
    alvo = url_for('lead.oportunidades.etapa2', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade)
    if current_app.htmx:
        if prop_form.validate():
            atualizar_preenchimento(prop_form, g.preenchimento)
            current_app.db.session.commit()
            return redirect(url_for('.etapa3', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade), code=307)
        return render_block('cadastro/proponente.html', 'content', prop_form=prop_form, alvo=alvo)

    return render_template('cadastro/proponente.html', prop_form=prop_form, alvo=alvo)


@oportunidades.post('/etapa3')
def etapa3():
    prop_form = Etapa3Form()
    alvo = url_for('lead.oportunidades.etapa3', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade)
    if current_app.htmx:
        if prop_form.validate():
            atualizar_preenchimento(prop_form, g.preenchimento)
            current_app.db.session.commit()
            return redirect(url_for('.etapa4', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade), code=307)
        return render_block('cadastro/proponente.html', 'content', prop_form=prop_form, alvo=alvo)

    return render_template('cadastro/proponente.html', prop_form=prop_form, alvo=alvo)


@oportunidades.post('/etapa4')
def etapa4():
    prop_form = Etapa4Form()
    alvo = url_for('lead.oportunidades.etapa4', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade)
    if current_app.htmx:
        if prop_form.validate():
            atualizar_preenchimento(prop_form, g.preenchimento)
            current_app.db.session.commit()
            return redirect(url_for('.etapa5', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade), code=307)
        return render_block('cadastro/proponente.html', 'content', prop_form=prop_form, alvo=alvo)

    return render_template('cadastro/proponente.html', prop_form=prop_form, alvo=alvo)


@oportunidades.post('/etapa5')
def etapa5():
    prop_form = Etapa5Form()
    alvo = url_for('lead.oportunidades.etapa5_add', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade)
    if [i for i in g.preenchimento.detalhes]:
        alvo2 = url_for('lead.oportunidades.etapa6', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade)
    else:
        alvo2 = None

    return render_block('cadastro/tabela.html', 'content', prop_form=prop_form, alvo=alvo, alvo2=alvo2)


@oportunidades.post('/etapa5_add')
def etapa5_add():
    prop_form = Etapa5Form()
    alvo = url_for('lead.oportunidades.etapa5_add', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade)
    if [i for i in g.preenchimento.detalhes]:
        alvo2 = url_for('lead.oportunidades.etapa6', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade)
    else:
        alvo2 = None
    if prop_form.validate():
        detalhe = Detalhes(**{key: value for key, value in prop_form.data.items()
                              if key != 'csrf_token'})
        g.preenchimento.detalhes.append(detalhe)
        current_app.db.session.commit()
    return render_block('cadastro/tabela.html', 'content', prop_form=prop_form, alvo=alvo, alvo2=alvo2)


@oportunidades.post('/etapa6')
def etapa6():
    prop_form = Etapa6Form()
    alvo = url_for('lead.oportunidades.etapa6', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade)
    if current_app.htmx:
        if prop_form.validate():
            atualizar_preenchimento(prop_form, g.preenchimento)
            current_app.db.session.commit()
            return redirect(url_for('.etapa7', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade), code=307)
        return render_block('cadastro/proponente.html', 'content', prop_form=prop_form, alvo=alvo)
    return render_template('cadastro/proponente.html', prop_form=prop_form, alvo=alvo)


@oportunidades.post('/etapa7')
def etapa7():
    prop_form = Etapa7Form()
    alvo = url_for('lead.oportunidades.etapa7', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade)
    if current_app.htmx:
        if prop_form.validate():
            atualizar_preenchimento(prop_form, g.preenchimento)
            current_app.db.session.commit()
            return redirect(url_for('.etapa8', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade), code=307)
        return render_block('cadastro/proponente.html', 'content', prop_form=prop_form, alvo=alvo)
    return render_template('cadastro/proponente.html', prop_form=prop_form, alvo=alvo)


@oportunidades.post('/etapa8')
def etapa8():
    prop_form = Etapa8Form()
    alvo = url_for('lead.oportunidades.etapa8', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade)
    if current_app.htmx:
        if prop_form.validate():
            atualizar_preenchimento(prop_form, g.preenchimento)
            current_app.db.session.commit()
            return redirect(url_for('.etapa9', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade), code=307)
            return redirect(url_for('lead.index', hashdd=g.cliente.links[0].link))
        flash("Nesta seção deverá ser preenchido a contrapartida social (Ou seja, dos 10% da verba destina ao CANS, 5% "
              "ficará para o CANS e os demais serão destinados a instituição descrita abaixo) -  Descreva a instituição",
              'primary')
        return render_block('cadastro/proponente.html', 'content', prop_form=prop_form, alvo=alvo)
    return render_template('cadastro/proponente.html', prop_form=prop_form, alvo=alvo)


@oportunidades.route('/etapa9', methods=['get', 'post'])
def etapa9():
    prop_form = DocumentoForm()
    alvo = url_for('lead.oportunidades.etapa9', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade)
    if current_app.htmx:
        if prop_form.validate():
            # atualizar_preenchimento(prop_form, g.preenchimento)
            # g.preenchimento.preenchido = True
            # current_app.db.session.commit()
            for arquivo in prop_form.docs.data:
                print(current_app.config['S3_ACCESS_KEY'])
                print(current_app.config['S3_SECRET_KEY'])
                nome = upload_s3(arquivo)


            return 'ok'
            return redirect(url_for('.etapa9', hashdd=g.cliente.links[0].link, oportunidade=g.oportunidade), code=307)
            return redirect(url_for('lead.index', hashdd=g.cliente.links[0].link))
        return render_block('cadastro/proponente.html', 'content', prop_form=prop_form, alvo=alvo, file=True)
    print('ue')
    return render_template('cadastro/proponente.html', prop_form=prop_form, alvo=alvo, file=True)



def configure(bp):
    bp.register_blueprint(oportunidades, url_prefix='/<oportunidade>')
