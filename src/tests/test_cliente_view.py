import pytest
from flask_login import current_user, logout_user

from conftest import C_CPF
from flask import url_for, session


def test_link_valido_deve_retornar_200_e_redirecionar_para_registrar(
    client, link1, app
):
    resposta = client.get(url_for("lead.oi", hashdd=link1), follow_redirects=True)
    assert resposta.status_code == 200
    assert resposta.request.path == url_for("lead.cliente_registrar", hashdd=link1)


def test_link_invalido_deve_retornar_404(client, gerar_cliente, app):
    link = app.hashid.encode(2)
    assert client.get(url_for("lead.oi", hashdd=link)).status_code == 404


def test_registrar_deve_renderizar_form_com_cpf_senha_e_confirmacao(client, link1):
    res = client.get(url_for("lead.cliente_registrar", hashdd=link1))
    assert res.status_code == 200
    assert b"cpf" in res.data
    assert b"senha" in res.data
    assert b"confirmar_senha" in res.data


@pytest.mark.parametrize(
    "data, erro",
    [
        ({"cpf": "212313212", "confirmar_senha": "12312312"}, "Coloque uma senha"),
        (
            {"senha": "212312312312", "confirmar_senha": "212312312312"},
            "Preencha o CPF",
        ),
        (
            {"cpf": "212313212", "senha": "212312312312", "confirmar_senha": "bb"},
            "As senhas não batem!",
        ),
        ({"senha": "123", "confirmar_senha": "123"}, "No mínimo 8 caracteres!"),
        (
            {
                "cpf": "333333",
                "senha": "212312312312",
                "confirmar_senha": "212312312312",
            },
            "CPF inválido",
        ),
    ],
)
def test_registrar_form_deve_retornar_erros_caso_campos_nao_sejam_preenchidos_corretamente(
    client, link1, data, erro
):
    res = client.post(
        url_for("lead.cliente_registrar", hashdd=link1),
        data=data,
        headers={"HX-Request": "true"},
        follow_redirects=True,
    )
    assert bytes(erro, "utf8") in res.data


def test_testing(client, gerar_cliente, link1):
    res = client.get(url_for('lead.testeuser', hashdd=link1))
    assert b'asd' == res.data


def test_registrar_deve_redirecionar_para_pagina_principal_caso_usuario_se_registre_com_sucesso(
    client, link1
):
    data = {"cpf": C_CPF, "senha": "212312312312", "confirmar_senha": "212312312312"}
    res = client.post(
        url_for("lead.cliente_registrar", hashdd=link1),
        data=data,
        headers={"HX-Request": "true"},
        follow_redirects=True,
    )
    assert res.request.path == url_for("lead.oi", hashdd=link1)


def test_pagina_principal_deve_redirecionar_para_login_caso_usuario_esteja_registrado_e_cliente_nao_esteja_logado(cliente_client, client, link1):
    logout_user()
    res = client.get(url_for('lead.oi', hashdd=link1), follow_redirects=True)
    assert res.status_code == 200
    assert res.request.path == url_for('lead.cliente_logar', hashdd=link1)
