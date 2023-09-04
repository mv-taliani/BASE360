import pytest
from flask import url_for
from flask_login import current_user
from wtforms import BooleanField

from conftest import C_CPF, C_NOME, C_CHECKS, C_TELEFONE, PROPOSTAS
from src.forms import link_form_builder
from src.models import Users, Cliente


def test_index_deve_retornar_302_quando_usuario_nao_estiver_logado(client):
    assert client.get(url_for('views.index')).status_code == 302


def test_index_deve_redirecionar_para_login_quando_usuario_nao_estiver_logado(client):
    assert client.get(url_for('views.index', follow_redirects=True)).location.split('?')[0] == url_for('auth.login')


@pytest.mark.parametrize('campo', [b'usuario', b'senha', b'lembrar'])
def test_login_deve_conter_formulario_para_logar(client, campo):
    assert campo in client.get(url_for('auth.login')).data


def test_tabela_users_deve_existir_no_banco_de_dados(database):
    user = Users(email='email@email.com', nome='teste', senha='1234')
    database.session.add(user)
    database.session.commit()
    assert user == Users.query.first()


def test_login_form_deve_validar_entrada_quando_invalida(client):
    assert client.post(url_for('auth.login_post'), data=dict(usuario='email@email.com')).status_code == 302


def test_login_form_deve_retornar_login_ou_senha_invalidos_quando_entrada_invalida(client):
    res = client.post(url_for('auth.login_post'), data=dict(usuario='email@email.com'), follow_redirects=True)
    assert b'Login ou senha' in res.data


def test_login_deve_logar_usuario_quando_ele_existir_e_a_senha_estiver_correta(client, criar_user):
    res = client.post(url_for('auth.login_post'), data=dict(usuario='email@email.com', senha='1234', lembrar=False),
                      follow_redirects=True)
    assert current_user.nome == 'teste'


def test_index_deve_recepcionar_usuario_quando_logado(logged_client):
    res = logged_client.get('/')
    # assert Users.query.first().id == 1
    # assert res.status_code == 200
    assert b'Bem vindo, test' in res.data


@pytest.mark.parametrize('campos', [('teste1', 'teste2', 'teste3',), ('batata1', 'batata2',)])
def test_link_form_builder_deve_montar_checkboxes_com_lista_de_strings_no_argumento(database, campos):
    form = link_form_builder(campos)
    assert all([getattr(form, i).label.text == i.upper() for i in campos])
    assert all([isinstance(getattr(form, i), BooleanField) for i in campos])


@pytest.mark.parametrize('oportunidade', [b'FIP', b'FIM', b'FIS', b'FIE', b'FIV', b'PAM', b'PAE', b'PIEDU'])
def test_vender_deve_retornar_form_criado_com_link_form_builder_contendo_as_oportunidades_da_base360(logged_client, oportunidade):
    res = logged_client.get(url_for('views.vender'))
    assert oportunidade in res.data


def test_link_form_deve_validar_entradas_quando_invalidas(logged_client):
    res = logged_client.post(url_for('api.gerar_link'), data=dict(cpf='40404040400404044004'))
    assert b'Coloque o nome do cliente' in res.data
    assert b'Insira o telefone do cliente!' in res.data
    assert b'CPF ou CNPJ muito longo' in res.data


def test_gerar_link_deve_cadastrar_cliente_quando_entrada_valida(logged_client):
    res = logged_client.post(url_for('api.gerar_link'), data=dict(cpf='123456789012', nome='Teste Client',
                                                                  telefone='1196767676776', check=['FIP', 'FIM']))

    assert '123456789012' == Cliente.query.first().cpf


def test_gerar_link_deve_cadastrar_link_do_cliente_quando_entrada_valida(gerar_cliente, app):
    assert Cliente.query.first().links


def test_link_do_client_deve_ser_id_do_cliente_no_banco_encriptado(gerar_cliente, app):
    cliente = Cliente.query.first()
    link = cliente.links
    assert app.hashid.decode(link[0].link)[0] == cliente.id


@pytest.mark.parametrize('oportunidade', ['FIP', 'FIM'])
def test_gerar_link_deve_acrescentar_oportunidades_selecionadas_ao_link_do_cliente(gerar_cliente, oportunidade):
    cliente = Cliente.query.first()
    assert oportunidade in [i.nome for i in cliente.links[0].propostas]


def test_gerar_link_deve_retornar_html_com_link_do_cliente(gerar_cliente):
    cliente = Cliente.query.first()
    link = cliente.links[0].link
    assert bytes(url_for('lead.oi', hashdd=link), 'utf-8') in gerar_cliente.data


def test_gerar_link_deve_redirecionar_para_pagina_do_cliente_caso_cliente_já_exista(gerar_cliente, gerar_cliente2):
    assert gerar_cliente2.status_code == 200


def test_pesquisar_deve_retornar_pagina_do_cliente_caso_cliente_exista(logged_client, gerar_cliente):
    assert logged_client.get(url_for('views.pesquisar', cpf='123456789012')).status_code == 200


@pytest.mark.parametrize('infos', [C_CPF, C_NOME, *C_CHECKS, C_TELEFONE])
def test_pesquisar_deve_conter_informações_do_cliente_na_página_quando_encontrado(logged_client, gerar_cliente, infos):
    res = logged_client.get(url_for('views.pesquisar', cpf=C_CPF))
    assert bytes(infos, 'utf-8') in res.data


def test_pesquisar_deve_redirecionar_para_vender_quando_cliente_nao_encontrado_e_hierarquia_maior_que_1(logged_client):
    res = logged_client.get(url_for('views.pesquisar', cpf='aleatorio'), follow_redirects=True)
    assert res.request.path == url_for('views.vender')
    assert b'Cliente inexistente' in res.data


def test_pesquisar_deve_redirecionar_para_vender_quando_cliente_nao_encontrado_e_hierarquia_igual_a_1(vendedor_client):
    res = vendedor_client.get(url_for('views.pesquisar', cpf='aleatorio'), follow_redirects=True)
    assert res.request.path == url_for('views.vender')
    assert b'Esse cliente pertence a outro vendendor ou inexiste' in res.data


def test_pesquisar_post_deve_redirecionar_para_pesquisar(logged_client, gerar_cliente):
    res = logged_client.post(url_for('views.pesquisar_post'), data=dict(cpf=C_CPF), follow_redirects=True)
    assert res.request.path == url_for('views.pesquisar', cpf=C_CPF)


@pytest.mark.parametrize('oportunidade', PROPOSTAS)
def test_permissoes_deve_retornar_form_com_todas_oportunidades_cadastradas(logged_client, gerar_cliente, oportunidade):
    res = logged_client.get(url_for('api.permissoes', id=1))
    assert bytes(oportunidade, 'utf-8') in res.data


@pytest.mark.parametrize('oportunidade', PROPOSTAS)
def test_editar_permissoes_deve_retornar_permissoes_atualizadas_do_cliente(logged_client, gerar_cliente, oportunidade):
    res = logged_client.post(url_for('api.editar_permissoes', id=1), data=dict(check=PROPOSTAS))
    assert bytes(oportunidade, 'utf-8') in res.data



