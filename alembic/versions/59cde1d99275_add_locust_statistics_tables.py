"""
Add Locust statistics tables.

Revision ID: 59cde1d99275
Revises:
Create Date: 2020-06-14 07:11:01.946038+00:00

"""


from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "59cde1d99275"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "test_run",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("test_plan", sa.String(length=32), nullable=False),
        sa.Column("profile", sa.String(length=32), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_on", sa.DateTime(timezone=True), nullable=False),
        sa.Column("started_on", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_on", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "request",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("run_id", sa.Integer(), nullable=False),
        sa.Column("greenlet_id", sa.Integer(), nullable=False),
        sa.Column("pid", sa.Integer(), nullable=False),
        sa.Column("method", sa.String(length=7), nullable=False),
        sa.Column("url", sa.String(), nullable=False),
        sa.Column("is_successful", sa.Boolean(), nullable=False),
        sa.Column("response_time", sa.Float(), nullable=False),
        sa.Column("response_length", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(("run_id",), ("test_run.id",)),
        sa.PrimaryKeyConstraint("id", "timestamp"),
    )
    op.create_table(
        "user_count",
        sa.Column("id", sa.Integer(), nullable=False, autoincrement=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("run_id", sa.Integer(), nullable=False),
        sa.Column("count", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(("run_id",), ("test_run.id",)),
        sa.PrimaryKeyConstraint("id", "timestamp"),
    )
    # ### end Alembic commands ###
    connection = op.get_bind()
    connection.execute("SELECT create_hypertable('request', 'timestamp')")
    connection.execute("SELECT create_hypertable('user_count', 'timestamp')")


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("user_count")
    op.drop_table("request")
    op.drop_table("test_run")
    # ### end Alembic commands ###