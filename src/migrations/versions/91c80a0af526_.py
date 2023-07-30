"""empty message

Revision ID: 91c80a0af526
Revises: 9c9c06c16240
Create Date: 2023-07-30 03:07:18.309983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91c80a0af526'
down_revision = '9c9c06c16240'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('instituição',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(length=100), nullable=True),
    sa.Column('cnpj', sa.String(length=19), nullable=True),
    sa.Column('contato', sa.String(length=50), nullable=True),
    sa.Column('dados_bancarios', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('instituição', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_instituição_id'), ['id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('instituição', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_instituição_id'))

    op.drop_table('instituição')
    # ### end Alembic commands ###
