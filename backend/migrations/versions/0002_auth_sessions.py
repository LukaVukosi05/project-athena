"""Add revocable sign-in sessions and external provider identities."""

from alembic import op
import sqlalchemy as sa

revision = "0002_auth_sessions"
down_revision = "0001_existing_core"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "auth_sessions",
        sa.Column("token_hash", sa.String(64), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_auth_sessions_user_id", "auth_sessions", ["user_id"])
    op.create_index("ix_auth_sessions_expires_at", "auth_sessions", ["expires_at"])
    op.create_table(
        "external_identities",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("provider", sa.String(16), nullable=False),
        sa.Column("subject", sa.String(255), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.UniqueConstraint("provider", "subject", name="uq_identity_subject"),
    )
    op.create_index(
        "ix_external_identities_user_id", "external_identities", ["user_id"]
    )


def downgrade():
    raise RuntimeError(
        "Auth downgrade requires an explicit data-retention and restore plan."
    )
