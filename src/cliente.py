from flask import (Blueprint, abort, current_app, g, redirect, render_template,
                   session, url_for)
from flask_htmx import make_response
from flask_login import current_user, login_user
from jinja2_fragments.flask import render_block
from src.auth import login_manager
from src.forms import ClienteLogin, ClienteRegis, ProponenteForm
from src.models import Cliente, Links, Users
from src.oportunidades import configure as configure_oportunidade

lead = Blueprint("lead", __name__)
configure_oportunidade(lead)


@login_manager.user_loader
def load_user(id_):
    return Cliente.query.get(int(id_))


@lead.url_value_preprocessor
def get_cliente(endpoint, values):
    hashh = values.pop("hashdd")
    id = current_app.hashid.decode(hashh)
    # if not id:
    #     return abort(404)
    link = Cliente.query.get_or_404(id[0])
    link.links[0].acessos += 1
    g.cliente = link
    g.hashdd = hashh
    session["link_id"] = link.links[0].id
    current_app.db.session.commit()


@lead.get("/testeuser")
def testeuser():
    return current_user.cpf


@lead.get("/")
def oi():
    if not g.cliente.senha:
        return redirect(url_for(".cliente_registrar", hashdd=g.hashdd))
    try:
        cpf = Cliente.query.get_or_404(session["user"]).cpf
        if cpf == g.cliente.cpf:
            return render_template("catalogo.html")
        return abort(404)
    except KeyError as e:
        print("batata", e)
        return redirect(url_for(".cliente_logar", hashdd=g.hashdd))


@lead.route("/login", methods=["GET", "POST"])
def cliente_logar():
    if session.get("user"):
        return redirect(url_for(".oi", hashdd=g.hashdd))
    form = ClienteLogin()
    if form.validate_on_submit():
        session["user"] = g.cliente.id
        resposta = make_response(redirect=url_for(".oi", hashdd=g.hashdd))
        return resposta
    return render_template(
        "cadastro/proponente.html",
        prop_form=form,
        alvo=url_for(".cliente_logar", hashdd=g.hashdd),
    )


@lead.route("/registrar", methods=["GET", "POST"])
def cliente_registrar():
    if g.cliente.senha:
        return redirect(url_for(".cliente_logar", hashdd=g.hashdd))
    form = ClienteRegis()
    if current_app.htmx:
        if form.validate_on_submit():
            if (
                not Cliente.query.filter_by(cpf=form.cpf.data)
                .join(Links)
                .filter_by(link=g.hashdd)
                .first()
            ):
                form.cpf.errors.append("CPF inválido")
            else:
                g.cliente.senha = form.senha.data
                current_app.db.session.commit()
                session["user"] = g.cliente.id
                return redirect(url_for(".oi", hashdd=g.hashdd))
        return render_block("cadastro/registrar.html", "content", reg_form=form)
    return render_template("cadastro/registrar.html", reg_form=form)


def configure(app):
    app.register_blueprint(lead, url_prefix="/vip/<hashdd>")
