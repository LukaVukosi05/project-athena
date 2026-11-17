"""Explicitly simulated billing. Live provider routes are not implemented."""

from datetime import timedelta
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, ConfigDict, StrictBool
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.auth.sessions import require_same_origin
from app.core.config import get_settings
from app.core.security import get_current_user
from app.db.database import get_db
from app.db.models.user import User
from app.db.models.subscription import TrialSubscription, BillingNotification
from app.billing import service
from app.billing.plan import plan_summary, PRICE_CENTS, TRIAL_DAYS, TERMS_VERSION

router = APIRouter()


def test_billing_only():
    settings = get_settings()
    if (
        settings.environment.casefold() != "development"
        or not settings.billing_test_mode
    ):
        raise HTTPException(
            503, "Test checkout is not enabled. Live payments are not connected."
        )


@router.get("/plan")
def offer():
    settings = get_settings()
    return {
        **plan_summary(),
        "test_checkout_enabled": settings.environment.casefold() == "development"
        and settings.billing_test_mode,
        "live_payments_enabled": False,
    }


@router.get("/status")
def subscription_status(
    response: Response,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    response.headers["Cache-Control"] = "no-store"
    row = db.get(TrialSubscription, user.id)
    notices = db.scalars(
        select(BillingNotification).where(BillingNotification.user_id == user.id)
    ).all()
    summary = service.subscription_summary(row)
    return {
        **summary,
        "has_access": bool(
            user.is_premium
            or (
                get_settings().environment.casefold() == "development"
                and get_settings().billing_test_mode
                and summary.get("has_test_access", False)
            )
        ),
        "notifications": [
            {
                "kind": n.kind,
                "due_at": service.utc(n.due_at).isoformat(),
                "delivery_state": n.delivery_state,
            }
            for n in notices
        ],
    }


class TestAuthorisation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    consent: StrictBool
    adult_payer: StrictBool
    terms_version: str
    outcome: str = "approved"


@router.post("/test/authorise", dependencies=[Depends(test_billing_only)])
def authorise(
    payload: TestAuthorisation,
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    require_same_origin(request)
    if not payload.consent or not payload.adult_payer:
        raise HTTPException(
            422, "An adult payer must agree to the trial and recurring price."
        )
    if payload.terms_version != TERMS_VERSION:
        raise HTTPException(
            409, "The offer changed. Refresh the checkout before continuing."
        )
    if payload.outcome not in {"approved", "declined"}:
        raise HTTPException(422, "Choose an approved or declined test outcome.")
    # One trial per account. Repeated callbacks never restart its clock.
    existing = db.get(TrialSubscription, user.id)
    if existing:
        return service.subscription_summary(existing)
    if payload.outcome == "declined":
        raise HTTPException(
            402,
            "Simulated payment-method authorisation declined. No trial has started.",
        )
    authorised = service.now()
    row = TrialSubscription(
        user_id=user.id,
        mode="test",
        method_reference="test_" + uuid4().hex,
        amount_cents=PRICE_CENTS,
        currency="ZAR",
        terms_version=TERMS_VERSION,
        consent_at=authorised,
        authorised_at=authorised,
        trial_ends_at=authorised + timedelta(days=TRIAL_DAYS),
    )
    db.add(row)
    for kind, due in (
        ("confirmation", authorised),
        ("trial_reminder", row.trial_ends_at - timedelta(days=7)),
    ):
        db.add(
            BillingNotification(
                user_id=user.id,
                kind=kind,
                due_at=due,
                delivery_state="test_preview_only",
            )
        )
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        row = db.get(TrialSubscription, user.id)
        if row is None:
            raise
    return service.subscription_summary(row)


def owned_test_row(db, user):
    row = db.get(TrialSubscription, user.id)
    if row is None or row.mode != "test":
        raise HTTPException(404, "Test subscription not found.")
    return row


@router.post("/cancel", dependencies=[Depends(test_billing_only)])
def cancel(
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    require_same_origin(request)
    row = owned_test_row(db, user)
    db.execute(
        update(TrialSubscription)
        .where(
            TrialSubscription.user_id == user.id,
            TrialSubscription.canceled_at.is_(None),
        )
        .values(canceled_at=service.effective_now(row))
    )
    db.commit()
    db.expire_all()
    return service.subscription_summary(db.get(TrialSubscription, user.id))


@router.post("/test/advance", dependencies=[Depends(test_billing_only)])
def advance_test_clock(
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    require_same_origin(request)
    row = owned_test_row(db, user)
    if row.first_charge_at is None and row.test_clock_at is None:
        row.test_clock_at = row.trial_ends_at
        db.commit()
    return service.subscription_summary(row)


@router.post("/test/first-charge", dependencies=[Depends(test_billing_only)])
def test_first_charge(
    request: Request,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    require_same_origin(request)
    row = owned_test_row(db, user)
    current = service.effective_now(row)
    if row.canceled_at:
        raise HTTPException(
            409, "This subscription was canceled. No payment will be simulated."
        )
    if current < service.utc(row.trial_ends_at):
        raise HTTPException(
            409, "The full 14-day trial must end before a payment can be simulated."
        )
    # Conditional update makes duplicate submissions idempotent and honours cancellation.
    db.execute(
        update(TrialSubscription)
        .where(
            TrialSubscription.user_id == user.id,
            TrialSubscription.canceled_at.is_(None),
            TrialSubscription.first_charge_at.is_(None),
        )
        .values(first_charge_at=current, paid_until=service.next_month(current))
    )
    db.commit()
    db.expire_all()
    return service.subscription_summary(db.get(TrialSubscription, user.id))
