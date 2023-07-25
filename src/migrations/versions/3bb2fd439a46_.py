"""empty message

Revision ID: 3bb2fd439a46
Revises: 815ac1ecc87b
Create Date: 2023-07-20 12:41:51.474997

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3bb2fd439a46'
down_revision = '815ac1ecc87b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('endereco',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cep', sa.String(length=8), nullable=True),
    sa.Column('uf', sa.String(length=2), nullable=True),
    sa.Column('cidade', sa.String(), nullable=True),
    sa.Column('bairro', sa.String(), nullable=True),
    sa.Column('rua', sa.String(), nullable=True),
    sa.Column('numero', sa.Integer(), nullable=True),
    sa.Column('cliente_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['cliente_id'], ['cliente.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('endereco', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_endereco_id'), ['id'], unique=False)

    with op.batch_alter_table('cliente', schema=None) as batch_op:
        batch_op.drop_index('ix_cliente_cpf')
        batch_op.create_index(batch_op.f('ix_cliente_cpf'), ['cpf'], unique=True)
        batch_op.create_unique_constraint('uq_rg', ['rg'])
        batch_op.drop_column('numero')
        batch_op.drop_column('cep')
        batch_op.drop_column('uf')
        batch_op.drop_column('cidade')
        batch_op.drop_column('rua')
        batch_op.drop_column('bairro')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cliente', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bairro', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('rua', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('cidade', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('uf', sa.VARCHAR(length=2), nullable=True))
        batch_op.add_column(sa.Column('cep', sa.VARCHAR(length=8), nullable=True))
        batch_op.add_column(sa.Column('numero', sa.INTEGER(), nullable=True))
        batch_op.drop_constraint('uq_rg', type_='unique')
        batch_op.drop_index(batch_op.f('ix_cliente_cpf'))
        batch_op.create_index('ix_cliente_cpf', ['cpf'], unique=False)

    with op.batch_alter_table('endereco', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_endereco_id'))

    op.drop_table('endereco')
    # ### end Alembic commands ###