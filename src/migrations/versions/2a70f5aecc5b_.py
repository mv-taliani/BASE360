"""empty message

Revision ID: 2a70f5aecc5b
Revises: 
Create Date: 2023-07-31 14:23:38.708450

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "2a70f5aecc5b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "propostas",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nome", sa.String(length=50), nullable=True),
        sa.Column("sobre", sa.String(), nullable=True),
        sa.Column("ativo", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("propostas", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_propostas_id"), ["id"], unique=False)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=150), nullable=False),
        sa.Column("nome", sa.String(length=25), nullable=False),
        sa.Column("senha", sa.String(), nullable=False),
        sa.Column("hierarquia", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "cliente",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nome", sa.String(length=60), nullable=True),
        sa.Column("nasc", sa.Date(), nullable=True),
        sa.Column("email", sa.String(length=50), nullable=True),
        sa.Column("cpf", sa.String(length=20), nullable=True),
        sa.Column("rg", sa.String(length=20), nullable=True),
        sa.Column("cadastrado", sa.DateTime(), nullable=True),
        sa.Column("senha", sa.String(), nullable=True),
        sa.Column("vendedor_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["vendedor_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("rg"),
    )
    with op.batch_alter_table("cliente", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_cliente_cpf"), ["cpf"], unique=True)
        batch_op.create_index(batch_op.f("ix_cliente_id"), ["id"], unique=False)

    op.create_table(
        "links",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("criada", sa.DateTime(), nullable=True),
        sa.Column("link", sa.String(), nullable=True),
        sa.Column("acessos", sa.Integer(), nullable=True),
        sa.Column("cliente_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["cliente_id"],
            ["cliente.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("links", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_links_id"), ["id"], unique=False)

    op.create_table(
        "telefone",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("telefone", sa.String(length=13), nullable=True),
        sa.Column("cliente_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["cliente_id"],
            ["cliente.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("telefone", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_telefone_id"), ["id"], unique=False)
        batch_op.create_index(
            batch_op.f("ix_telefone_telefone"), ["telefone"], unique=False
        )

    op.create_table(
        "links_e_props",
        sa.Column("link_id", sa.Integer(), nullable=True),
        sa.Column("proposta_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["link_id"],
            ["links.id"],
        ),
        sa.ForeignKeyConstraint(
            ["proposta_id"],
            ["propostas.id"],
        ),
    )
    op.create_table(
        "preenchimento",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("proponente", sa.String(length=90), nullable=True),
        sa.Column("responsavel", sa.String(length=90), nullable=True),
        sa.Column("cnpj", sa.String(length=19), nullable=True),
        sa.Column("cpf", sa.String(length=15), nullable=True),
        sa.Column("endereco", sa.String(), nullable=True),
        sa.Column("aporte", sa.Numeric(precision=11, scale=2), nullable=True),
        sa.Column("lote", sa.String(length=13), nullable=True),
        sa.Column("identidade", sa.String(), nullable=True),
        sa.Column("analise", sa.String(), nullable=True),
        sa.Column("objetivos", sa.String(), nullable=True),
        sa.Column("swot", sa.String(), nullable=True),
        sa.Column("marketing", sa.String(), nullable=True),
        sa.Column("futuro", sa.String(), nullable=True),
        sa.Column("observações", sa.String(), nullable=True),
        sa.Column("preenchido", sa.Boolean(), nullable=True),
        sa.Column("link_id", sa.Integer(), nullable=False),
        sa.Column("proposta_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["link_id"],
            ["links.id"],
        ),
        sa.ForeignKeyConstraint(
            ["proposta_id"],
            ["propostas.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("preenchimento", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_preenchimento_id"), ["id"], unique=False)

    op.create_table(
        "arquivos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nome_original", sa.String(), nullable=True),
        sa.Column("nome_aws", sa.String(), nullable=True),
        sa.Column("preenchimento_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["preenchimento_id"],
            ["preenchimento.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("arquivos", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_arquivos_id"), ["id"], unique=False)

    op.create_table(
        "detalhes",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("descricao", sa.String(), nullable=True),
        sa.Column("periodo", sa.String(length=50), nullable=True),
        sa.Column("valor", sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column("justificativa", sa.String(length=200), nullable=True),
        sa.Column("preenchimento_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["preenchimento_id"],
            ["preenchimento.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("detalhes", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_detalhes_id"), ["id"], unique=False)

    op.create_table(
        "instituição",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nome", sa.String(length=100), nullable=True),
        sa.Column("cnpj", sa.String(length=19), nullable=True),
        sa.Column("contato", sa.String(length=50), nullable=True),
        sa.Column("dados_bancarios", sa.String(length=100), nullable=True),
        sa.Column("preenchimento_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["preenchimento_id"],
            ["preenchimento.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("instituição", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_instituição_id"), ["id"], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("instituição", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_instituição_id"))

    op.drop_table("instituição")
    with op.batch_alter_table("detalhes", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_detalhes_id"))

    op.drop_table("detalhes")
    with op.batch_alter_table("arquivos", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_arquivos_id"))

    op.drop_table("arquivos")
    with op.batch_alter_table("preenchimento", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_preenchimento_id"))

    op.drop_table("preenchimento")
    op.drop_table("links_e_props")
    with op.batch_alter_table("telefone", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_telefone_telefone"))
        batch_op.drop_index(batch_op.f("ix_telefone_id"))

    op.drop_table("telefone")
    with op.batch_alter_table("links", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_links_id"))

    op.drop_table("links")
    with op.batch_alter_table("cliente", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_cliente_id"))
        batch_op.drop_index(batch_op.f("ix_cliente_cpf"))

    op.drop_table("cliente")
    op.drop_table("users")
    with op.batch_alter_table("propostas", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_propostas_id"))

    op.drop_table("propostas")
    # ### end Alembic commands ###
