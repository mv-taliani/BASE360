"""empty message

Revision ID: 80ee804f029f
Revises: 91c80a0af526
Create Date: 2023-07-30 03:09:46.736286

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '80ee804f029f'
down_revision = '91c80a0af526'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('instituição', schema=None) as batch_op:
        batch_op.add_column(sa.Column('preenchimento_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('preenchimento_id', 'preenchimento', ['preenchimento_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('instituição', schema=None) as batch_op:
        batch_op.drop_constraint('preenchimento_id', type_='foreignkey')
        batch_op.drop_column('preenchimento_id')

    # ### end Alembic commands ###