from functools import wraps
from flask_login import current_user
from flask import current_app, g
import boto3
import io
import uuid
from werkzeug.utils import secure_filename


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


def _connect_s3():
    s3 = boto3.client(
        's3',
        aws_access_key_id=current_app.config['S3_ACCESS_KEY'],
        aws_secret_access_key=current_app.config['S3_SECRET_KEY'],
        region_name='us-east-2'
    )
    return s3


def _set_filename(cpf, proposta):
    def inner(namename):
        filename = str(uuid.uuid4().hex)
        filename = filename + f'{cpf}_{proposta}.pdf'
        return filename
    return inner


def upload_s3(file, set_filename):
    file_stream = io.BytesIO(file.read())
    filename = set_filename(file.filename)
    s3 = _connect_s3()
    s3.upload_fileobj(file_stream, current_app.config['S3_BUCKET_NAME'], filename)
    file_stream.seek(0)
    return filename


def get_s3(filename):
    ...
