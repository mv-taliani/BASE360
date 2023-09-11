from src import create_app
from src.models import Propostas, Cliente, db, Users
from flask import url_for
import pytest

PROPOSTAS = ['FIP', 'FIM', 'FIS', 'FIE', 'FIV', 'PAM', 'PAE', 'PIEDU']

C_CPF = '123456789012'
C_NOME = 'Teste Client'
C_TELEFONE = '1196767676776'
C_CHECKS = ['FIP', 'FIM']



@pytest.fixture(scope='module')
def app():
    app = create_app()
    return app


@pytest.fixture()
def database(app):
    with app.app_context():
        db.create_all()
        db.create_all()
        for prop in PROPOSTAS:
            p = Propostas(nome=prop, sobre='sobre sobre sobre sobre sobre sobre sobre sobre', ativo=True)
            db.session.add(p)
        db.session.commit()
        yield db
        db.drop_all()


@pytest.fixture()
def criar_user(database):
    user = Users(email='email@email.com', nome='teste', senha='1234', hierarquia=4)
    database.session.add(user)
    database.session.commit()
    return user


@pytest.fixture()
def criar_vendedor(database):
    user = Users(email='vendedor@email.com', nome='v_teste', senha='1234')
    database.session.add(user)
    database.session.commit()
    return user


@pytest.fixture()
def logged_client(client, criar_user):
    with client.session_transaction() as sess:
        res = client.post(url_for('auth.login_post'), data=dict(usuario='email@email.com', senha='1234', lembrar=False),
                          follow_redirects=True)
    yield client


@pytest.fixture()
def vendedor_client(client, criar_vendedor):
    with client.session_transaction() as sess:
        res = client.post(url_for('auth.login_post'), data=dict(usuario='vendedor@email.com', senha='1234', lembrar=False),
                          follow_redirects=True)
    yield client


@pytest.fixture()
def gerar_cliente(logged_client):
    res = logged_client.post(url_for('api.gerar_link'), data=dict(cpf=C_CPF, nome=C_NOME,
                                                                  telefone=C_TELEFONE, check=C_CHECKS),
                             follow_redirects=True)
    return res


@pytest.fixture()
def gerar_cliente2(logged_client):
    res = logged_client.post(url_for('api.gerar_link'), data=dict(cpf=C_CPF, nome=C_NOME,
                                                                  telefone=C_TELEFONE, check=C_CHECKS),
                             follow_redirects=True)
    return res
