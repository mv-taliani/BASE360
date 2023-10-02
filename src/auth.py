from flask import (Blueprint, current_app, flash, redirect, render_template,
                   url_for)
from flask_login import current_user, login_required, login_user, logout_user, LoginManager
from werkzeug.security import check_password_hash

from src.forms import LoginForm, RegisForm
from src.models import Users

auth = Blueprint("auth", __name__)
login_manager = LoginManager()


@auth.get("/login")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("views.index"))
    form = LoginForm()
    return render_template("login.html", form=form)


@auth.post("/login")
def login_post():
    form = LoginForm()
    if form.validate():
        email = form.usuario.data
        senha = form.senha.data
        remember = form.lembrar.data
        user = Users.query.filter_by(email=email).first()
        if user and check_password_hash(user.senha, senha):
            login_user(user, remember=remember)
            return redirect(url_for("views.index"))
    flash("Login ou senha inválidos!", "danger")
    return redirect(url_for(".login"))


@auth.route("/registrar", methods=["GET", "POST"])
@login_required
def registrar():
    if not current_user.hierarquia > 1:
        return redirect(url_for("views.index"))
    form = RegisForm()
    if form.validate_on_submit():
        user = Users(email=form.email.data, nome=form.nome.data, senha=form.senha.data)
        current_app.db.session.add(user)
        current_app.db.session.commit()
        flash(f"{form.nome.data.split()[0]} registrado!", "success")
    return render_template("criarusuario.html", form=form)


# @auth.post('/registrar')
# def registrar_post():
#     form = RegisForm(request.form)
#     if form.validate_on_submit():
#         return f'{form.nome.data}'
#     return render_template('criarusuario.html', form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


def configure(app):
    app.register_blueprint(auth)
