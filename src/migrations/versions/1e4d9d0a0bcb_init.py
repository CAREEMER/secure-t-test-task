"""init

Revision ID: 1e4d9d0a0bcb
Revises:
Create Date: 2022-10-25 22:40:16.251065

"""
import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "1e4d9d0a0bcb"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("CREATE EXTENSION IF NOT EXISTS ltree;")
    op.create_table(
        "user",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("time_created", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("time_updated", sa.DateTime(timezone=True), nullable=True),
        sa.Column("username", sa.Text(), nullable=False),
        sa.Column("password", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_id"), "user", ["id"], unique=False)
    op.create_index(op.f("ix_user_username"), "user", ["username"], unique=True)
    op.create_table(
        "post",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("time_created", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("time_updated", sa.DateTime(timezone=True), nullable=True),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("author_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("deleted", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_post_id"), "post", ["id"], unique=False)
    op.create_table(
        "session",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("time_created", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("time_updated", sa.DateTime(timezone=True), nullable=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_session_id"), "session", ["id"], unique=False)
    op.create_table(
        "comment",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("time_created", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=True),
        sa.Column("time_updated", sa.DateTime(timezone=True), nullable=True),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("author_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("post_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("node_path", sqlalchemy_utils.types.ltree.LtreeType(), nullable=False),
        sa.Column("deleted", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["author_id"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["post_id"],
            ["post.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_comment_id"), "comment", ["id"], unique=False)
    op.create_index("ix_nodes_path", "comment", ["node_path"], unique=False, postgresql_using="gist")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_nodes_path", table_name="comment", postgresql_using="gist")
    op.drop_index(op.f("ix_comment_id"), table_name="comment")
    op.drop_table("comment")
    op.drop_index(op.f("ix_session_id"), table_name="session")
    op.drop_table("session")
    op.drop_index(op.f("ix_post_id"), table_name="post")
    op.drop_table("post")
    op.drop_index(op.f("ix_user_username"), table_name="user")
    op.drop_index(op.f("ix_user_id"), table_name="user")
    op.drop_table("user")
    # ### end Alembic commands ###
