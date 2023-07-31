from functools import wraps
from flask_login import current_user
from flask import current_app, g, abort, redirect, url_for
import boto3
import io
import uuid


def validar(tipo, valor):
    try:
        tipo.validate(valor)
        return True
    except:
        return False


def somente_cliente(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            if current_user.cpf == g.cliente.cpf:
                return func(*args, **kwargs)
        except:
            return abort(404)
    return inner


def redirecionar_view(url, atributo, oportunidade):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            if getattr(g, atributo) == oportunidade:
                return redirect(url_for(url))
            return func(*args, **kwargs)
        return inner
    return wrapper



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


def upload_s3(file):
    file_stream = io.BytesIO(file.read())
    filename = file.filename
    s3 = _connect_s3()
    s3.upload_fileobj(file_stream, current_app.config['S3_BUCKET_NAME'], filename)
    return filename


def get_s3(filename):
    file_stream = io.BytesIO()
    s3 = _connect_s3()
    s3.download_fileobj(current_app.config['S3_BUCKET_NAME'], filename, file_stream)
    file_stream.seek(0)
    return file_stream
