from flask import Blueprint, g, abort
from src.models import Cliente

oportunidades = Blueprint('oportunidades', __name__)


@oportunidades.url_value_preprocessor
def get_oportunidade(endpoint, values):
    oportunidade = values.pop('oportunidade')
    if oportunidade in [prop.nome for prop in g.cliente.links[0].propostas]:
        g.oportunidade = oportunidade
    else:
        abort(404)


@oportunidades.get('/')
def index():
    return 'oi'


def configure(bp):
    bp.register_blueprint(oportunidades, url_prefix='/<oportunidade>')
