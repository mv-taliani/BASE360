from dynaconf import FlaskDynaconf
from flask import Flask
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension
from flask_htmx import HTMX
import flask_excel
from hashids import Hashids
from src.auth import configure as auth_config
from src.views import configure as views_config
from src.models import configure as db_config
from src.adm import configure as adm_config
from src.api import configure as api_config
from src.models import Users, Cliente
from src.cliente import configure as cliente_config


def create_app():
    app = Flask(__name__)
    FlaskDynaconf(app, env='development')
    # app.config.from_prefixed_env()
    db_config(app)
    app.config['DEBUG_TB_TEMPLATE_EDITOR_ENABLED'] = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    toolbar = DebugToolbarExtension()
    toolbar.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Você precisa estar logado!'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id_):
        return Users.query.get(int(id_)) or Cliente.query.get(int(id_))

    app.htmx = HTMX(app)
    hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])
    app.hashid = hashids

    flask_excel.init_excel(app)

    adm_config(app)
    api_config(app)
    auth_config(app)
    views_config(app)
    cliente_config(app)

    return app