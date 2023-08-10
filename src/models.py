from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    nome = db.Column(db.String(25), nullable=False)
    senha = db.Column(db.String, nullable=False)
    hierarquia = db.Column(db.Integer, nullable=False, default=1)

    def __init__(self, email, nome, senha, hierarquia=1):
        self.email = email
        self.nome = nome
        self.senha = generate_password_hash(senha, method='sha512')
        self.hierarquia = hierarquia

    def __repr__(self):
        return f'User {self.nome}'


class Cliente(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, index=True)
    nome = db.Column(db.String(60))
    nasc = db.Column(db.Date)
    email = db.Column(db.String(50))
    cpf = db.Column(db.String(20), index=True, unique=True)
    rg = db.Column(db.String(20), unique=True)
    cadastrado = db.Column(db.DateTime(timezone=False), default=db.func.now())
    senha = db.Column(db.String)

    vendedor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    vendedor = db.relationship('Users', backref=db.backref('clientes', lazy='dynamic'))

    def __repr__(self):
        return f'Cliente: {self.cpf}'


class Telefone(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    telefone = db.Column(db.String(13), index=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)

    cliente = db.relationship('Cliente', backref='telefones')

    def __repr__(self):
        return f'Telefone: {self.telefone}'


class Propostas(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    nome = db.Column(db.String(50))
    sobre = db.Column(db.String)
    ativo = db.Column(db.Boolean, default=False)

    def __str__(self):
        return str(self.nome)


links_e_props = db.Table('links_e_props',
                         db.Column('link_id', db.Integer, db.ForeignKey('links.id')),
                         db.Column('proposta_id', db.Integer, db.ForeignKey('propostas.id'))
                         )


class Links(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    criada = db.Column(db.DateTime(timezone=False), default=db.func.now())
    link = db.Column(db.String)
    acessos = db.Column(db.Integer, default=0)

    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)

    cliente = db.relationship('Cliente', backref=db.backref('links', lazy='dynamic'))
    propostas = db.relationship('Propostas', secondary=links_e_props, backref='links')


class Preenchimento(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    proponente = db.Column(db.String(90))
    responsavel = db.Column(db.String(90))
    cnpj = db.Column(db.String(19))
    cpf = db.Column(db.String(15))
    endereco = db.Column(db.String)
    aporte = db.Column(db.Numeric(11, 2))
    lote = db.Column(db.String(13))
    identidade = db.Column(db.String)
    analise = db.Column(db.String)
    objetivos = db.Column(db.String)
    swot = db.Column(db.String)
    marketing = db.Column(db.String)
    futuro = db.Column(db.String)
    observações = db.Column(db.String)
    preenchido = db.Column(db.Boolean, default=False)

    link_id = db.Column(db.Integer, db.ForeignKey(Links.id), nullable=False)
    proposta_id = db.Column(db.Integer, db.ForeignKey(Propostas.id), nullable=False)

    links = db.relationship('Links', backref=db.backref('preenchimentos', lazy='dynamic'))
    propostas = db.relationship('Propostas', backref=db.backref('preenchimentos', lazy='dynamic'))


class Arquivos(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    nome_original = db.Column(db.String)
    nome_aws = db.Column(db.String)
    preenchimento_id = db.Column(db.Integer, db.ForeignKey('preenchimento.id'), nullable=False)

    preenchimento = db.relationship('Preenchimento', backref=db.backref('arquivos', lazy='dynamic'))


class Instituição(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    nome = db.Column(db.String(100))
    cnpj = db.Column(db.String(19))
    contato = db.Column(db.String(50))
    dados_bancarios = db.Column(db.String(100))

    preenchimento_id = db.Column(db.Integer, db.ForeignKey(Preenchimento.id), nullable=False)

    preenchimentos = db.relationship('Preenchimento', backref=db.backref('insituicao', lazy='dynamic'))


class Detalhes(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    descricao = db.Column(db.String)
    periodo = db.Column(db.String(50))
    valor = db.Column(db.Numeric(10, 2))
    justificativa = db.Column(db.String(200))

    preenchimento_id = db.Column(db.Integer, db.ForeignKey(Preenchimento.id), nullable=False)

    preenchimento = db.relationship('Preenchimento', backref=db.backref('detalhes', lazy='dynamic'))


def configure(app):
    db.init_app(app)
    Migrate(app, db)
    app.db = db
