"""Persist test trial terms, dates, cancellation and notification previews."""

from alembic import op
import sqlalchemy as sa

revision = "0003_trial_subscriptions"
down_revision = "0002_auth_sessions"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "trial_subscriptions",
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("mode", sa.String(16), nullable=False),
        sa.Column("method_reference", sa.String(80), nullable=False),
        sa.Column("terms_version", sa.String(80), nullable=False),
        sa.Column("amount_cents", sa.Integer(), nullable=False),
        sa.Column("currency", sa.String(3), nullable=False),
        *[
            sa.Column(name, sa.DateTime(timezone=True), nullable=False)
            for name in ("consent_at", "authorised_at", "trial_ends_at")
        ],
        *[
            sa.Column(name, sa.DateTime(timezone=True), nullable=True)
            for name in (
                "canceled_at",
                "first_charge_at",
                "paid_until",
                "test_clock_at",
            )
        ]
    )
    op.create_table(
        "billing_notifications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("kind", sa.String(32), nullable=False),
        sa.Column("due_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("delivery_state", sa.String(32), nullable=False),
        sa.UniqueConstraint("user_id", "kind", name="uq_billing_notice"),
    )


def downgrade():
    raise RuntimeError(
        "Billing downgrade requires an explicit retention and restore plan."
    )
