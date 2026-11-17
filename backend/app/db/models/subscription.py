"""Test subscriptions and durable notification previews. Never stores card data."""

from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.database import Base


class TrialSubscription(Base):
    __tablename__ = "trial_subscriptions"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    mode: Mapped[str] = mapped_column(String(16), nullable=False)
    method_reference: Mapped[str] = mapped_column(String(80), nullable=False)
    terms_version: Mapped[str] = mapped_column(String(80), nullable=False)
    amount_cents: Mapped[int] = mapped_column(Integer, nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    consent_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    authorised_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    trial_ends_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    canceled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    first_charge_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    paid_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    test_clock_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class BillingNotification(Base):
    __tablename__ = "billing_notifications"
    __table_args__ = (UniqueConstraint("user_id", "kind", name="uq_billing_notice"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    kind: Mapped[str] = mapped_column(String(32), nullable=False)
    due_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    delivery_state: Mapped[str] = mapped_column(String(32), nullable=False)
