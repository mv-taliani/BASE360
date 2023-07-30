from flask import Blueprint, current_app, g, render_template, redirect, url_for
from flask_login import current_user
from src.models import Links
from src.forms import ClienteRegis, ProponenteForm
from src.oportunidades import configure as configure_oportunidade

lead = Blueprint('lead', __name__)
configure_oportunidade(lead)


@lead.url_value_preprocessor
def get_cliente(endpoint, values):
    hashh = values.pop('hashdd')
    id = current_app.hashid.decode(hashh)
    # if not id:
    #     return abort(404)
    link = Links.query.get_or_404(id[0])
    link.acessos += 1
    g.cliente = link.cliente
    current_app.db.session.commit()


@lead.get('/')
def oi():
    # if not g.cliente.senha:
    #     return render_template('cadastro/registrar.html', reg_form=reg_form)
    # try:
    #     cpf = current_user.cpf
    #     if cpf == g.cliente.cpf:
    #         return render_template('catalogo.html')
    # except:
    #     return 'oi'
    reg_form = ClienteRegis()
    return render_template('catalogo.html')

    # return render_template('cadastro/registrar.html', reg_form=reg_form)


def configure(app):
    app.register_blueprint(lead, url_prefix='/vip/<hashdd>')
