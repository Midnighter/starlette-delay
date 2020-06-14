"""
Add table for measured delay.

Revision ID: 71ee4b0b302d
Revises: 59cde1d99275
Create Date: 2020-06-14 11:51:23.866475+00:00

"""


from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "71ee4b0b302d"
down_revision = "59cde1d99275"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "delay",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True),
        sa.Column("run_id", sa.Integer(), nullable=False),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("delay", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(("run_id",), ("test_run.id",)),
        sa.PrimaryKeyConstraint("id", "timestamp"),
    )
    op.get_bind().execute("SELECT create_hypertable('delay', 'timestamp')")


def downgrade():
    op.drop_table("delay")
