from datetime import date, datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.models import EstadoPago, Payment

#Data access layer for payments. Insert-only for GESTOR; admin update is audited.

def create_payment(db: Session, **fields) -> Payment:
    db_payment = Payment(**fields)
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


def get_payment_by_id(db: Session, payment_id: int) -> Optional[Payment]:

    return db.query(Payment).filter(Payment.id == payment_id).first()


def list_payments(
    db: Session,
    member_id: Optional[int] = None,
    inscription_id: Optional[int] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
) -> list[Payment]:

    query = db.query(Payment)
    if member_id is not None:
        query = query.filter(Payment.member_id == member_id)
    if inscription_id is not None:
        query = query.filter(Payment.inscription_id == inscription_id)
    if from_date is not None:
        query = query.filter(Payment.payment_date >= from_date)
    if to_date is not None:
        query = query.filter(Payment.payment_date <= to_date)
    return query.order_by(Payment.payment_date.desc(), Payment.id.desc()).all()


def get_active_payment_for_period(
    db: Session, inscription_id: int, 
    due_date: date
) -> Optional[Payment]:
    #A cancelled (ANULADO) payment does not block a new one for the same period.
    return (
        db.query(Payment)
        .filter(
            Payment.inscription_id == inscription_id,
            Payment.due_date == due_date,
            Payment.status != EstadoPago.ANULADO,
        )
        .first()
    )


def list_active_payments_by_inscription(db: Session, inscription_id: int) -> list[Payment]:
    return (
        db.query(Payment)
        .filter(
            Payment.inscription_id == inscription_id,
            Payment.status != EstadoPago.ANULADO,
        )
        .all()
    )


def update_payment_audit(db: Session, payment: Payment, fields: dict, admin_id: int) -> Payment:
    #Admin correction: overwrite the touched fields plus the audit columns.
    for field, value in fields.items():
        setattr(payment, field, value)
    payment.updated_by_id = admin_id
    payment.updated_at = datetime.utcnow()
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment
