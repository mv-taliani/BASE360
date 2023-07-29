"""empty message

Revision ID: 2a418fb35341
Revises: 31ecfb4e71cd
Create Date: 2023-07-28 17:34:24.560429

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a418fb35341'
down_revision = '31ecfb4e71cd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('propostas', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sobre', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('propostas', schema=None) as batch_op:
        batch_op.drop_column('sobre')

    # ### end Alembic commands ###