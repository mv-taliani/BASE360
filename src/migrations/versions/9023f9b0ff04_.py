"""empty message

Revision ID: 9023f9b0ff04
Revises: 00cddc5b3863
Create Date: 2023-09-05 11:09:46.222490

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "9023f9b0ff04"
down_revision = "00cddc5b3863"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("preenchimento", schema=None) as batch_op:
        batch_op.add_column(sa.Column("contador", sa.String(length=90), nullable=True))
        batch_op.add_column(
            sa.Column("coordenador", sa.String(length=90), nullable=True)
        )
        batch_op.add_column(sa.Column("gestor", sa.String(length=90), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("preenchimento", schema=None) as batch_op:
        batch_op.drop_column("gestor")
        batch_op.drop_column("coordenador")
        batch_op.drop_column("contador")

    # ### end Alembic commands ###
