from flask import url_for


def login(client):
    with client.application.test_request_context():
        return client.post(
            url_for("auth.login_post"),
            data=dict(usuario="email@email.com", senha="1234"),
        )
