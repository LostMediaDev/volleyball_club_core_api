


from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.depends import require_role
from app.database import get_db
from app.schemas import (
    BillingQuoteResponse,
    PaymentAdminUpdate,
    PaymentCreate,
    PaymentResponse,
)
from app.services import service_payments

#Payment (cobros) endpoints. Thin controllers: validation + delegation to services.

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@router.get("/quote", response_model=BillingQuoteResponse)
def get_payment_quote(
    member_id: Optional[int] = None,
    dni: Optional[str] = None,
    current_user=Depends(require_role("GESTOR")),
    db: Session = Depends(get_db),
):
    return service_payments.quote(db, member_id=member_id, dni=dni)


@router.post("", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def register_payment(
    data: PaymentCreate,
    current_user=Depends(require_role("GESTOR")),
    db: Session = Depends(get_db),
):
    return service_payments.register_payment(db, data, current_user)


@router.get("", response_model=list[PaymentResponse])
def list_payments(
    member_id: Optional[int] = None,
    dni: Optional[str] = None,
    inscription_id: Optional[int] = None,
    from_date: Optional[date] = None,
    to_date: Optional[date] = None,
    current_user=Depends(require_role("GESTOR")),
    db: Session = Depends(get_db),
):
    return service_payments.list_payments(
        db,
        member_id=member_id,
        dni=dni,
        inscription_id=inscription_id,
        from_date=from_date,
        to_date=to_date,
    )


@router.get("/{payment_id}", response_model=PaymentResponse)
def get_payment(
    payment_id: int,
    current_user=Depends(require_role("GESTOR")),
    db: Session = Depends(get_db),
):
    return service_payments.get_payment(db, payment_id)


@router.patch("/{payment_id}", response_model=PaymentResponse)
def admin_update_payment(
    payment_id: int,
    data: PaymentAdminUpdate,
    current_user=Depends(require_role("ADMIN")),
    db: Session = Depends(get_db),
):
    return service_payments.admin_update_payment(db, payment_id, data, current_user)


