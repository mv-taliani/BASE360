from flask import url_for


def test_link_valido_deve_retornar_200_e_redirecionar_para_registrar(client, gerar_cliente, app):
    link = app.hashid.encode(1)
    resposta = client.get(url_for('lead.oi', hashdd=link), follow_redirects=True)
    assert resposta.status_code == 200
    assert resposta.request.path == url_for('lead.cliente_registrar', hashdd=link)


def test_link_invalido_deve_retornar_404(client, gerar_cliente, app):
    link = app.hashid.encode(2)
    assert client.get(url_for('lead.oi', hashdd=link)).status_code == 404


def test_registrar_deve_renderizar_form_com_cpf_senha_e_confirmacao(client, gerar_cliente):
    ...
