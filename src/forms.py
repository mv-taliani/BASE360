from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, BooleanField, StringField, DateField, IntegerField, SelectField
from wtforms.validators import DataRequired, InputRequired, Length, EqualTo, Email, ValidationError
from wtforms_sqlalchemy.fields import QuerySelectField
from pydantic_br import CPF, CNPJ, FieldInvalidError
from src.models import Origem, Campanha, Propostas, Users, Cliente
from src.utils import validar
from src.constants import UFS


class LoginForm(FlaskForm):
    usuario = EmailField('Usuário', validators=[DataRequired(message='Precisamos do seu email!')])
    senha = PasswordField('Senha', validators=[DataRequired(message='Precisamos da sua senha!')])
    lembrar = BooleanField('Lembrar-se')


class RegisForm(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired('Faltou o nome!'),
                                           Length(min=1, max=25, message='Nome muito longo!')])
    email = EmailField('Email', validators=[InputRequired(message='O usuário precisa logar!'),
                                            Email('Insira um email válido!')])
    senha = PasswordField('Senha', validators=[InputRequired('O usuário precisa de senha!'),
                                               Length(min=8, message='No mínimo 8 caracteres!')])
    confirmar_senha = PasswordField('Confirmar senha', validators=[EqualTo('senha', message='As senhas não batem!')])

    def validate(self, extra_validators=None):
        initial_validation = super(RegisForm, self).validate()
        user = Users.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email já registrado")
            return False
        if not initial_validation:
            return False

        return True

class ClienteForm(FlaskForm):
    cpf = StringField('CPF', validators=[InputRequired(), Length(min=11, max=20, message='CPF Inválido')])
    rg = StringField('RG', validators=[InputRequired(), Length(min=7, max=20)])
    nome = StringField('Nome Completo', validators=[InputRequired(), Length(min=1, max=60, message='Nome muito longo!')])
    nasc = DateField('Data de Nascimento', format='%d-%m-%Y', validators=[InputRequired()])
    email = EmailField('Email', validators=[InputRequired()])
    telefone = StringField('Telefone', validators=[InputRequired()])


class EnderecoForm(FlaskForm):
    cep = StringField('CEP', validators=[InputRequired(), Length(min=8, max=8)])
    uf = SelectField('UF', choices=[(uf, uf) for uf in UFS], validators=[InputRequired()])
    bairro = StringField('Bairro', validators=[InputRequired()])
    cidade = StringField('Cidade', validators=[InputRequired()])
    rua = StringField('Rua', validators=[InputRequired()])
    numero = IntegerField('Número', validators=[InputRequired()])


class LinkFormBase(FlaskForm):
    cpf = StringField('CPF', validators=[InputRequired('Preencha o CPF')])
    nome = StringField('Nome', validators=[InputRequired('Coloque o nome do cliente.')])
    telefone = StringField('Telefone', validators=[InputRequired('Insira o telefone do cliente!')])


def link_form_builder(servicos, **kwargs):
    class LinkForm(LinkFormBase):
        ...
    for i, servico in enumerate(servicos):
        setattr(LinkForm, f'{servico}', BooleanField(label=str(servico).upper(), name='check'))
    return LinkForm(**kwargs)


class ClienteRegis(FlaskForm):
    cpf = StringField('CPF', validators=[InputRequired('Preencha o CPF')])
    senha = PasswordField('Senha', validators=[InputRequired('Você precisa de uma senha!'),
                                               Length(min=8, message='No mínimo 8 caracteres!')])
    confirmar_senha = PasswordField('Confirmar senha', validators=[EqualTo('senha', message='As senhas não batem!')])

    def validate(self, extra_validators=None):
        initial_validation = super(ClienteRegis, self).validate()
        if not initial_validation:
            return False
        user = Cliente.query.filter_by(cpf=self.cpf.data.replace('-', '').replace('.', '').replace('/', '')).first()
        if not user:
            self.cpf.errors.append("CPF inválido")
            return False
        return True


def validate_proponente(form, field):
    field.data = field.data.replace('-', '').replace('.', '').replace('/', '')
    if not validar(CNPJ, field.data) or validar(CPF, field.data):
        raise ValidationError('CPF ou CNPJ inválido!')


class ProponenteForm(FlaskForm):
    proponente = StringField('Proponente', validators=[InputRequired('Precisamos do proponente!'), validate_proponente])
