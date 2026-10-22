#OP CODE START
#OP Business logic for the payment domain.
#OP Computes what a member owes from their active inscription + plan, and records charges.

import calendar
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional

from sqlalchemy.orm import Session

from app.crud import crud_members, crud_payments
from app.models import FrecuenciaPlan, Payment
from app.schemas import (
    BillingPeriod,
    BillingQuoteResponse,
    PaymentAdminUpdate,
    PaymentCreate,
)
from app.services.service_members import (
    BusinessRuleError,
    NotFoundError,
    _resolve_member,
)

#OP CODE - Number of months each billing cycle covers.
FREQUENCY_MONTHS = {
    FrecuenciaPlan.MENSUAL: 1,
    FrecuenciaPlan.CUATRIMESTRAL: 4,
    FrecuenciaPlan.ANUAL: 12,
}

_HUNDRED = Decimal("100")


def _days_in_month(year: int, month: int) -> int:
    return calendar.monthrange(year, month)[1]


def _add_months(source: date, months: int) -> date:
    month_index = source.month - 1 + months
    year = source.year + month_index // 12
    month = month_index % 12 + 1
    day = min(source.day, _days_in_month(year, month))
    return date(year, month, day)


def _frequency_months(frequency: FrecuenciaPlan) -> int:
    return FREQUENCY_MONTHS[frequency]


def _combined_discount(db: Session, member_id: int, plan) -> Decimal:
    #OPPlan frequency discount + every active member discount, capped at 100%.
    total = Decimal(str(plan.discount_percentage or 0))
    for discount in crud_members.get_active_discounts_by_member(db, member_id):
        total += Decimal(str(discount.percentage))
    return min(total, _HUNDRED)


def _period_amount(plan, percentage: Decimal) -> Decimal:
    amount = Decimal(str(plan.base_amount)) * (_HUNDRED - percentage) / _HUNDRED
    return amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _schedule(inscription, until: date) -> tuple[list[date], Optional[date]]:
    #OP CODE - Due dates from start_date stepping by the plan frequency, up to `until`.
    #OP CODE - Returns (due_dates_so_far, next_due_date_after_the_window).
    months = _frequency_months(inscription.plan.frequency)
    due_dates: list[date] = []
    current = inscription.start_date
    while current <= until and (inscription.end_date is None or current <= inscription.end_date):
        due_dates.append(current)
        current = _add_months(current, months)

    next_due: Optional[date] = current
    if inscription.end_date is not None and current > inscription.end_date:
        next_due = None
    return due_dates, next_due


def quote(db: Session, member_id: Optional[int] = None, dni: Optional[str] = None) -> BillingQuoteResponse:
    member = _resolve_member(db, member_id, dni)
    inscription = crud_members.get_active_inscription_by_member(db, member.id)
    if inscription is None:
        raise NotFoundError(f"Member {member.id} has no active inscription")

    plan = inscription.plan
    percentage = _combined_discount(db, member.id, plan)
    amount = _period_amount(plan, percentage)

    today = date.today()
    schedule, next_due = _schedule(inscription, today)
    paid_dates = {
        payment.due_date
        for payment in crud_payments.list_active_payments_by_inscription(db, inscription.id)
    }

    unpaid = [due for due in schedule if due not in paid_dates]
    unpaid_periods = [
        BillingPeriod(
            due_date=due,
            amount=amount,
            days_overdue=max(0, (today - due).days),
        )
        for due in unpaid
    ]
    total_due = (amount * len(unpaid)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    days_overdue = max((period.days_overdue for period in unpaid_periods), default=0)
    if unpaid_periods:
        status = "OVERDUE" if days_overdue > 0 else "DUE"
        next_due_date = unpaid_periods[0].due_date
    else:
        status = "UP_TO_DATE"
        next_due_date = next_due

    return BillingQuoteResponse(
        member_id=member.id,
        dni=member.dni,
        inscription_id=inscription.id,
        plan_id=plan.id,
        plan_name=plan.name,
        frequency=plan.frequency,
        base_amount=plan.base_amount,
        discount_percentage=percentage,
        amount_due=amount,
        total_due=total_due,
        next_due_date=next_due_date,
        status=status,
        days_overdue=days_overdue,
        unpaid_periods=unpaid_periods,
    )


def _next_payable_due_date(db: Session, inscription) -> date:
    #OP CODE - First period without an active payment; falls back to the upcoming one.
    today = date.today()
    schedule, next_due = _schedule(inscription, today)
    paid_dates = {
        payment.due_date
        for payment in crud_payments.list_active_payments_by_inscription(db, inscription.id)
    }
    for due in schedule:
        if due not in paid_dates:
            return due
    if next_due is not None:
        return next_due
    raise BusinessRuleError("The inscription has no pending periods to charge")


def register_payment(db: Session, data: PaymentCreate, current_user) -> Payment:
    member = _resolve_member(db, data.member_id, data.dni)
    if not member.is_active:
        raise BusinessRuleError("Cannot register a payment for an inactive member")

    inscription = crud_members.get_active_inscription_by_member(db, member.id)
    if inscription is None:
        raise NotFoundError(f"Member {member.id} has no active inscription")

    plan = inscription.plan
    percentage = _combined_discount(db, member.id, plan)
    amount = _period_amount(plan, percentage)

    due_date = data.due_date or _next_payable_due_date(db, inscription)

    if crud_payments.get_active_payment_for_period(db, inscription.id, due_date) is not None:
        raise BusinessRuleError(f"Period {due_date} was already paid")

    return crud_payments.create_payment(
        db,
        member_id=member.id,
        inscription_id=inscription.id,
        amount=amount,
        discount_percentage_applied=percentage,
        method=data.method,
        payment_date=data.payment_date or date.today(),
        due_date=due_date,
        notes=data.notes,
        registered_by_id=current_user.id,
    )


def list_payments(
    db: Session,
    member_id: Optional[int] = None,
    dni: Optional[str] = None,
    inscription_id: Optional[int] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
) -> list[Payment]:
    if dni is not None:
        member = crud_members.get_member_by_dni(db, dni)
        if member is None:
            raise NotFoundError(f"Member with dni {dni} was not found")
        member_id = member.id
    return crud_payments.list_payments(
        db,
        member_id=member_id,
        inscription_id=inscription_id,
        from_date=from_date,
        to_date=to_date,
    )


def get_payment(db: Session, payment_id: int) -> Payment:
    payment = crud_payments.get_payment_by_id(db, payment_id)
    if payment is None:
        raise NotFoundError(f"Payment with id {payment_id} was not found")
    return payment


def admin_update_payment(
    db: Session, payment_id: int, data: PaymentAdminUpdate, admin_user
) -> Payment:
    payment = get_payment(db, payment_id)
    fields = data.model_dump(exclude_unset=True)
    return crud_payments.update_payment_audit(db, payment, fields, admin_user.id)

#OP CODE END
