"""empty message

Revision ID: 825582ccf8cf
Revises: 454c4774712f
Create Date: 2023-09-08 13:02:28.041967

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "825582ccf8cf"
down_revision = "454c4774712f"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "recebimento",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("mes", sa.String(length=15), nullable=True),
        sa.Column("valor", sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column("detalhe_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["detalhe_id"],
            ["detalhes.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("recebimento", schema=None) as batch_op:
        batch_op.create_index(batch_op.f("ix_recebimento_id"), ["id"], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("recebimento", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_recebimento_id"))

    op.drop_table("recebimento")
    # ### end Alembic commands ###
