from functools import wraps
from flask_login import current_user
from flask import current_app, g


def validar(tipo, valor):
    try:
        tipo.validate(valor)
        return True
    except:
        return False


def somente_cliente(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if current_user == g.cliente:
            return func(*args, **kwargs)
        return current_app.login_manager.unauthorized()
    return inner


def atualizar_preenchimento(form, model):
    for key, value in form.data.items():
        if key != 'csrf_token':
            setattr(model, key, value)

