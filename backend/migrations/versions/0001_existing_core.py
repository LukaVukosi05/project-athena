"""Baseline the pre-auth-patch user and practice tables."""

from alembic import op
import sqlalchemy as sa

revision = "0001_existing_core"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("email", sa.String(320), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("grade", sa.String(16), nullable=False),
        sa.Column("curriculum_mode", sa.String(16), nullable=False),
        sa.Column("role", sa.String(16), nullable=False),
        sa.Column("is_premium", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_table(
        "practice_sessions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column("lesson_id", sa.String(80), nullable=False),
        sa.Column("responses", sa.JSON(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )
    op.create_index("ix_practice_sessions_user_id", "practice_sessions", ["user_id"])


def downgrade():
    raise RuntimeError(
        "Destructive baseline downgrade is disabled. Restore a verified backup instead."
    )
