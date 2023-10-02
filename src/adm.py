from flask import Blueprint, current_app
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from werkzeug.security import generate_password_hash

from src.models import (Arquivos, Cliente, Detalhes, Instituição, Links,
                        Preenchimento, Propostas, Telefone, Users, db)


class MyAdminIndexView(AdminIndexView):
    # def is_accessible(self):
    #     return current_user.is_authenticated and current_user.hierarquia >= 4
    ...


admin = Admin(
    name="Administrador", template_mode="bootstrap3", index_view=MyAdminIndexView()
)


class MyView(ModelView):
    # def is_accessible(self):
    #     return current_user.is_authenticated and current_user.hierarquia >= 3
    ...


class TelefoneView(ModelView):
    column_list = ["telefone", "cliente"]

    def is_accessible(self):
        return current_user.is_authenticated and current_user.hierarquia >= 3


class UsersView(MyView):
    can_export = True

    # def is_accessible(self):
    #    return current_user.is_authenticated and current_user.hierarquia >= 3

    def _on_model_change(self, form, model, is_created):
        model.senha = generate_password_hash(model.senha, method="sha512")


admin.add_view(UsersView(Users, db.session))
admin.add_view(MyView(Cliente, db.session, "Cliente"))
admin.add_view(TelefoneView(Telefone, db.session, "Telefone"))
admin.add_view(MyView(Propostas, db.session, "Propostas"))
admin.add_view(MyView(Links, db.session, "Links"))
admin.add_view(MyView(Preenchimento, db.session, "Preenchimento"))
admin.add_view(MyView(Detalhes, db.session, "Detalhes"))
admin.add_view(MyView(Instituição, db.session, "Instituição"))
admin.add_view(MyView(Arquivos, db.session, "Arquivos"))


def configure(app):
    admin.init_app(app)
