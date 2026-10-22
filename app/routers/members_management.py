from typing import Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.depends import require_role
from app.database import get_db
from app.schemas import (
    ApplyDiscountRequest,
    AssignPlanRequest,
    DiscountResponse,
    InscriptionResponse,
    MemberCreate,
    MemberResponse,
    MemberUpdate,
)
from app.services import service_members

#Member management endpoints. 
#Thin controllers: validation and delegation to services.

router = APIRouter(
    prefix="/members",
    tags=["Members"],
)


@router.post("", response_model=MemberResponse, status_code=status.HTTP_201_CREATED)
def create_member(
    data: MemberCreate,
    current_user=Depends(require_role("GESTOR")),
    db: Session = Depends(get_db),
):
    return service_members.create_member(db, data)


@router.get("", response_model=list[MemberResponse])
def list_members(
    is_active: Optional[bool] = None,
    current_user=Depends(require_role("GESTOR")),
    db: Session = Depends(get_db),
):
    return service_members.list_members(db, is_active=is_active)


@router.get("/dni/{dni}", response_model=MemberResponse)
def get_member_by_dni(
    dni: str,
    current_user=Depends(require_role("GESTOR")),
    db: Session = Depends(get_db),
):
    return service_members.get_member_by_dni(db, dni)


@router.post("/assign-plan", response_model=InscriptionResponse, status_code=status.HTTP_201_CREATED)
def assign_plan(
    data: AssignPlanRequest,
    current_user=Depends(require_role("GESTOR")),
    db: Session = Depends(get_db),
):
    return service_members.assign_plan(db, data)


@router.post("/discounts", response_model=DiscountResponse, status_code=status.HTTP_201_CREATED)
def apply_discount(
    data: ApplyDiscountRequest,
    current_user=Depends(require_role("GESTOR")),
    db: Session = Depends(get_db),
):
    return service_members.apply_discount(db, data)


@router.patch("/discounts/{discount_id}/deactivate", response_model=DiscountResponse)
def deactivate_discount(
    discount_id: int,
    current_user=Depends(require_role("GESTOR")),
    db: Session = Depends(get_db),
):
    return service_members.deactivate_discount(db, discount_id)


@router.get("/{member_id}", response_model=MemberResponse)
def get_member(
    member_id: int,
    current_user=Depends(require_role("GESTOR")),
    db: Session = Depends(get_db),
):
    return service_members.get_member(db, member_id)


@router.put("/{member_id}", response_model=MemberResponse)
def update_member(
    member_id: int,
    data: MemberUpdate,
    current_user=Depends(require_role("GESTOR")),
    db: Session = Depends(get_db),
):
    return service_members.update_member(db, member_id, data)


@router.delete("/{member_id}", response_model=MemberResponse)
def delete_member(
    member_id: int,
    current_user=Depends(require_role("GESTOR")),
    db: Session = Depends(get_db),
):
    return service_members.delete_member(db, member_id)

