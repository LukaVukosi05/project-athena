"""Deterministic Grade 12 finance calculations; values remain unrounded by default."""
from __future__ import annotations

from math import log


def periodic_rate(nominal_annual_rate: float, periods_per_year: int) -> float:
    if periods_per_year <= 0:
        raise ValueError("periods_per_year must be positive")
    return nominal_annual_rate / periods_per_year


def compound_value(principal: float, rate: float, periods: float) -> float:
    if principal < 0 or periods < 0 or rate <= -1:
        raise ValueError("invalid compound-value parameters")
    return principal * (1 + rate) ** periods


def simple_value(principal: float, rate: float, periods: float) -> float:
    if principal < 0 or periods < 0:
        raise ValueError("invalid simple-value parameters")
    return principal * (1 + rate * periods)


def reducing_balance(principal: float, rate: float, periods: float) -> float:
    if not 0 <= rate < 1:
        raise ValueError("depreciation rate must be from 0 up to 1")
    return compound_value(principal, -rate, periods)


def straight_line(principal: float, rate: float, periods: float) -> float:
    value = principal * (1 - rate * periods)
    if value < 0:
        raise ValueError("straight-line model produces a negative value")
    return value


def effective_annual_rate(nominal_annual_rate: float, periods_per_year: int) -> float:
    return (1 + periodic_rate(nominal_annual_rate, periods_per_year)) ** periods_per_year - 1


def future_value_annuity(payment: float, rate: float, payments: int) -> float:
    if payments < 1 or rate == 0:
        raise ValueError("positive payment count and non-zero rate required")
    return payment * ((1 + rate) ** payments - 1) / rate


def present_value_annuity(payment: float, rate: float, payments: int) -> float:
    if payments < 1 or rate == 0:
        raise ValueError("positive payment count and non-zero rate required")
    return payment * (1 - (1 + rate) ** -payments) / rate


def periods_for_growth(initial: float, target: float, rate: float) -> float:
    if initial <= 0 or target <= 0 or rate <= -1 or rate == 0:
        raise ValueError("positive amounts and a valid non-zero rate required")
    return log(target / initial) / log(1 + rate)
