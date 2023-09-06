from flask import Blueprint, current_app, g, render_template, redirect, url_for, session
from flask_htmx import make_response
from flask_login import current_user, login_user
from jinja2_fragments.flask import render_block

from src.models import Links, Users, Cliente
from src.forms import ClienteRegis, ProponenteForm, ClienteLogin
from src.oportunidades import configure as configure_oportunidade

lead = Blueprint('lead', __name__)
configure_oportunidade(lead)


@lead.url_value_preprocessor
def get_cliente(endpoint, values):
    hashh = values.pop('hashdd')
    id = current_app.hashid.decode(hashh)
    # if not id:
    #     return abort(404)
    link = Cliente.query.get_or_404(id[0])
    link.links[0].acessos += 1
    g.cliente = link
    g.hashdd = hashh
    session['link_id'] = link.links[0].id
    current_app.db.session.commit()


@lead.get('/')
def oi():
    if not g.cliente.senha:
        return redirect(url_for('.cliente_registrar', hashdd=g.hashdd))
    try:
        cpf = Cliente.query.get_or_404(session['user']).cpf
        if cpf == g.cliente.cpf:
            return render_template('catalogo.html')
    except Exception as e:
        print('batata', e)
        return redirect(url_for('.cliente_logar', hashdd=g.hashdd))


@lead.route('/login', methods=['GET', 'POST'])
def cliente_logar():
    if session.get('user'):
        return redirect(url_for('.oi', hashdd=g.hashdd))
    form = ClienteLogin()
    if form.validate_on_submit():
        session['user'] = g.cliente.id
        resposta = make_response(redirect=url_for('.oi', hashdd=g.hashdd))
        return resposta
    return render_template('cadastro/proponente.html', prop_form=form, alvo=url_for('.cliente_logar', hashdd=g.hashdd))


@lead.route('/registrar', methods=['GET', 'POST'])
def cliente_registrar():
    if g.cliente.senha:
        return redirect(url_for('.cliente_logar', hashdd=g.hashdd))
    form = ClienteRegis()
    if current_app.htmx:
        if form.validate():
            g.cliente.senha = form.senha.data
            current_app.db.session.commit()
            session['user'] = g.cliente.id
            return redirect(url_for('.oi', hashdd=g.hashdd))
        return render_block('cadastro/registrar.html', 'content', reg_form=form)
    return render_template('cadastro/registrar.html', reg_form=form)


def configure(app):
    app.register_blueprint(lead, url_prefix='/vip/<hashdd>')
