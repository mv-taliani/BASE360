from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from werkzeug.datastructures import FileStorage
from wtforms import MultipleFileField, EmailField, PasswordField, BooleanField, StringField, DateField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Length, EqualTo, Email, ValidationError, StopValidation
from collections import abc
from pydantic_br import CPF, CNPJ
from src.models import Users, Cliente
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
    cpf = StringField('CPF', validators=[InputRequired('Preencha o CPF'), Length(max=18, message='CPF ou CNPJ muito '
                                                                                                 'longo')])
    nome = StringField('Nome', validators=[InputRequired('Coloque o nome do cliente.')])
    telefone = StringField('Telefone', validators=[InputRequired('Insira o telefone do cliente!'), Length(max=13, message='Telefone muito longo')])


def link_form_builder(servicos, **kwargs):
    class LinkForm(LinkFormBase):
        ...
    for i, servico in enumerate(servicos):
        setattr(LinkForm, f'{servico}', BooleanField(label=str(servico).upper(), name='check'))
    return LinkForm(**kwargs)


class ClienteLogin(FlaskForm):
    senha = PasswordField('Senha', validators=[InputRequired('Você precisa logar')])


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


def validate_valor(form, field):
    try:
        val = float(field.data)
        return val
    except ValueError:
        raise ValidationError('Deve ser um número separado por ponto')


class ProponenteForm(FlaskForm):
    proponente = StringField('Proponente', validators=[InputRequired('Precisamos do proponente!')])
    responsavel = StringField('Responsável Legal - Se CNPJ')
    cnpj = StringField('CNPJ')
    cpf = StringField('CPF', validators=[InputRequired('Precisamos do CPF')])
    endereco = StringField('Endereço (se empresa, deve ser o mesmo do contrato)', validators=[InputRequired('Precisamos do endereço')])
    aporte = StringField('Valor do aporte (total do contrato)', validators=[InputRequired('Precisamos do valor'), validate_valor])
    lote = StringField('Lote de pagamento', validators=[InputRequired('Precisamos do lote')])

    def validate(self, extra_validators=None):
        initial_validation = super(ProponenteForm, self).validate()
        if not initial_validation:
            return False
        if validar(CNPJ, self.proponente) and not self.responsavel.data:
            print('batata')
            self.responsavel.errors.append('CNPJ necessita de um responsável legal!')
            return False
        if self.cnpj and validar(CNPJ, self.cnpj):
            self.cnpj.errors.append('CNPJ inválido!')
            return False
        return True


def proponente_form(oportunidade):
    form = ProponenteForm()
    if oportunidade != "FIP":
        delattr(form, 'cnpj')
    return form


class Etapa1Form(FlaskForm):
    identidade = TextAreaField("""Determine a identidade organizacional (Nesta seção, deverá ser fornecida uma visão geral do seu negócio. Assim, precisará considerar aspectos que o tornem único.
A identidade deve levar como base a Misão, Visão e Valores da empresa)
Missão: É a razão pela qual a sua empresa existe
Visão: É onde você quer chegar com a sua empresa pensando em longo prazo
Valores: São os princípios inegociáveis.""", validators=[InputRequired('Precisamos da sua identidade organizacional')])


class Etapa2Form(FlaskForm):
    analise = TextAreaField("Análise do mercado de atuação do seu negócios. Sobre você e/ou sua empresa se já for "
                           "estabelecido (A ideia nesta seção é de unificar o mercado que pretende atuar ou já atua com "
                           "seu projeto, e também falar sobre mercado alvo, tendências, crescimento e vantagens do "
                           "mercado de atuação)", validators=[InputRequired('Precisamos da análise do mercado')])


class Etapa3Form(FlaskForm):
    objetivos = TextAreaField("Quais são os objetivos de negócio? (Os objetivos de negócios são tudo o que você pretende "
                           "alcançar com o seu projeto, fale do geral até o específico.)",
                           validators=[InputRequired('Precisamos dos objetivos do seu negócio')])


class Etapa4Form(FlaskForm):
    swot = TextAreaField("Nessa seção deverá ser preenchido a análise SWOT",
                           validators=[InputRequired('Precisamos da análise SWOT')])



class Etapa5Form(FlaskForm):
    descricao = TextAreaField('Descrição', validators=[InputRequired('Preencha a descrição')])
    periodo = StringField('Período', validators=[InputRequired('Preencha o período'), Length(max=50)])
    valor = StringField('Valor', validators=[InputRequired('Preencha o valor em R$'), validate_valor])
    justificativa = StringField('Justificativa', validators=[InputRequired('Preencha a justificativa'), Length(max=200)])


class Etapa6Form(FlaskForm):
    marketing = TextAreaField("Plano de marketing e estratégias de continuidade do seu projeto (Aqui deverá ser "
                              "preenchido o planejamento de estratégia para alavancagem do produto/empresa e como sua "
                              "empresa permanecerá ativa após o término do recurso)",
                              validators=[InputRequired('Precisamos do plano de marketing!')])


class Etapa7Form(FlaskForm):
    futuro = TextAreaField("Nesta seção deverá ser preenchido o resumo de planos futuros (Se pretende ter algum negócio"
                           "social e se tem planos de expansão e afins)",
                           validators=[InputRequired('Precisamos do resumo de planos futuros')])


def validate_cnpj(form, field):
    if not validar(CNPJ, field.data):
        raise ValidationError('CNPJ inválido')


class Etapa8Form(FlaskForm):
    nome = StringField('Nome', validators=[InputRequired('Precisamos do nome')])
    cnpj = StringField('CNPJ', validators=[InputRequired('Precisamos do CNPJ'), validate_cnpj])
    contato = StringField('Contato', validators=[InputRequired('Precisamos do contato')])
    dados_bancarios = TextAreaField('Dados Bancários', validators=[InputRequired('Precisamos dos dados bancários'),
                                    Length(min=1, max=100)])


def validar_extensao(extensoes):
    def validate_doc(form, field):
        if not field.data:
            raise ValidationError('Precisamos dos documentos!')

        for dado in field.data:
            print(dado)
            filename: str = dado.filename.lower()
            if not all(filename.endswith('.' + x) for x in extensoes):
                raise ValidationError('Precisamos que esteja em PDF')
    return validate_doc


class MultipleFileAllowed:
    """Validates that the uploaded file is allowed by a given list of
    extensions or a Flask-Uploads :class:`~flaskext.uploads.UploadSet`.

    :param upload_set: A list of extensions or an
        :class:`~flaskext.uploads.UploadSet`
    :param message: error message

    You can also use the synonym ``file_allowed``.
    """

    def __init__(self, upload_set, message=None):
        self.upload_set = upload_set
        self.message = message

    def __call__(self, form, field):
        if not (all(isinstance(data, FileStorage) for data in field.data) and field.data):
            for i in field.data:
                print(i.filename)
            raise StopValidation('Precisamos que esteja em PDF')

        for data in field.data:
            filename = data.filename.lower()

            if isinstance(self.upload_set, abc.Iterable):
                if any(filename.endswith("." + x) for x in self.upload_set):
                    return

                raise StopValidation(
                    self.message
                    or field.gettext(
                        "File does not have an approved extension: {extensions}"
                    ).format(extensions=", ".join(self.upload_set))
                )

            if not self.upload_set.file_allowed(field.data, filename):
                raise StopValidation(
                    self.message
                    or field.gettext("File does not have an approved extension.")
                )


class DocumentoForm(FlaskForm):
    docs = MultipleFileField('Documentos necessários', validators=[InputRequired('Precisamos dos documentos'),
                                                                   MultipleFileAllowed(['pdf'], 'Apenas PDF\'s')])


class EtapaFinalForm(FlaskForm):
    observações = TextAreaField('Observações ')