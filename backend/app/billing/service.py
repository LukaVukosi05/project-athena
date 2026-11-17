"""Pure lifecycle rules. The test clock never changes the real system clock."""

import calendar
from datetime import datetime, timezone


def utc(value):
    return (
        value.replace(tzinfo=timezone.utc)
        if value.tzinfo is None
        else value.astimezone(timezone.utc)
    )


def now():
    return datetime.now(timezone.utc)


def effective_now(row):
    return max(now(), utc(row.test_clock_at)) if row.test_clock_at else now()


def next_month(value):
    value = utc(value)
    month = value.month % 12 + 1
    year = value.year + (value.month == 12)
    return value.replace(
        year=year, month=month, day=min(value.day, calendar.monthrange(year, month)[1])
    )


def subscription_summary(row):
    if row is None:
        return {"status": "not_started", "mode": "test", "real_money_charged": False}
    current = effective_now(row)
    end = utc(row.trial_ends_at)
    access_until = utc(row.paid_until) if row.paid_until else end
    status = (
        "active_test"
        if row.first_charge_at and current < access_until
        else "trialing" if current < end else "trial_ended"
    )
    if row.canceled_at:
        status = "canceled"
    return {
        "status": status,
        "mode": row.mode,
        "real_money_charged": False,
        "amount_cents": row.amount_cents,
        "currency": row.currency,
        "authorised_at": utc(row.authorised_at).isoformat(),
        "trial_ends_at": end.isoformat(),
        "access_until": access_until.isoformat(),
        "has_test_access": current < access_until,
        "first_charge_at": (
            utc(row.first_charge_at).isoformat() if row.first_charge_at else None
        ),
        "test_clock_at": (
            utc(row.test_clock_at).isoformat() if row.test_clock_at else None
        ),
        "canceled_at": utc(row.canceled_at).isoformat() if row.canceled_at else None,
        "terms_version": row.terms_version,
    }
