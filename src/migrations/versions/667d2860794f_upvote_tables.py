"""+upvote tables

Revision ID: 667d2860794f
Revises: 82e70a3f48ff
Create Date: 2022-10-21 23:01:14.083603

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "667d2860794f"
down_revision = "82e70a3f48ff"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "postupvote",
        sa.Column("uuid", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("user_uuid", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("post_uuid", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("positive", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["post_uuid"],
            ["post.uuid"],
        ),
        sa.ForeignKeyConstraint(
            ["user_uuid"],
            ["user.uuid"],
        ),
        sa.PrimaryKeyConstraint("uuid"),
    )
    op.create_index(op.f("ix_postupvote_post_uuid"), "postupvote", ["post_uuid"], unique=False)
    op.create_index(op.f("ix_postupvote_user_uuid"), "postupvote", ["user_uuid"], unique=False)
    op.create_index(op.f("ix_postupvote_uuid"), "postupvote", ["uuid"], unique=False)
    op.create_table(
        "commentupvote",
        sa.Column("uuid", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("user_uuid", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("comment_uuid", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("positive", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["comment_uuid"],
            ["comment.uuid"],
        ),
        sa.ForeignKeyConstraint(
            ["user_uuid"],
            ["user.uuid"],
        ),
        sa.PrimaryKeyConstraint("uuid"),
    )
    op.create_index(op.f("ix_commentupvote_comment_uuid"), "commentupvote", ["comment_uuid"], unique=False)
    op.create_index(op.f("ix_commentupvote_user_uuid"), "commentupvote", ["user_uuid"], unique=False)
    op.create_index(op.f("ix_commentupvote_uuid"), "commentupvote", ["uuid"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_commentupvote_uuid"), table_name="commentupvote")
    op.drop_index(op.f("ix_commentupvote_user_uuid"), table_name="commentupvote")
    op.drop_index(op.f("ix_commentupvote_comment_uuid"), table_name="commentupvote")
    op.drop_table("commentupvote")
    op.drop_index(op.f("ix_postupvote_uuid"), table_name="postupvote")
    op.drop_index(op.f("ix_postupvote_user_uuid"), table_name="postupvote")
    op.drop_index(op.f("ix_postupvote_post_uuid"), table_name="postupvote")
    op.drop_table("postupvote")
    # ### end Alembic commands ###