#OP CODE START
#OP CODE - Business logic for member management.
#OP CODE - Orchestrates the crud layer and raises domain errors (mapped to HTTP in main.py).

from typing import Optional

from sqlalchemy.orm import Session

from app.crud import crud_members, crud_plans
from app.models import Discount, Inscription, Member, Plan
from app.schemas import (
    ApplyDiscountRequest,
    AssignPlanRequest,
    MemberCreate,
    MemberUpdate,
    PlanCreate,
)


#OP CODE - Domain errors. The router stays thin; main.py translates these to HTTP.
class ServiceError(Exception):
    status_code = 400

    def __init__(self, detail: str):
        self.detail = detail
        super().__init__(detail)


class NotFoundError(ServiceError):
    status_code = 404


class ConflictError(ServiceError):
    status_code = 409


class BusinessRuleError(ServiceError):
    status_code = 400


def list_members(db: Session, is_active: Optional[bool] = None) -> list[Member]:
    return crud_members.get_all_members(db, is_active=is_active)


def get_member(db: Session, member_id: int) -> Member:
    member = crud_members.get_member_by_id(db, member_id)
    if member is None:
        raise NotFoundError(f"Member with id {member_id} was not found")
    return member


def get_member_by_dni(db: Session, dni: str) -> Member:
    member = crud_members.get_member_by_dni(db, dni)
    if member is None:
        raise NotFoundError(f"Member with dni {dni} was not found")
    return member


def create_member(db: Session, data: MemberCreate) -> Member:
    if crud_members.get_member_by_dni(db, data.dni):
        raise ConflictError(f"A member with dni {data.dni} already exists")
    if crud_members.get_member_by_email(db, data.email):
        raise ConflictError(f"A member with email {data.email} already exists")
    return crud_members.create_member(db, data)


def update_member(db: Session, member_id: int, data: MemberUpdate) -> Member:
    member = get_member(db, member_id)

    if data.email is not None:
        existing = crud_members.get_member_by_email(db, data.email)
        if existing is not None and existing.id != member.id:
            raise ConflictError(f"A member with email {data.email} already exists")

    return crud_members.update_member(db, member, data)


def delete_member(db: Session, member_id: int) -> Member:
    member = get_member(db, member_id)
    if not member.is_active:
        raise BusinessRuleError(f"Member with id {member_id} is already inactive")
    return crud_members.soft_delete_member(db, member)


def assign_plan(db: Session, data: AssignPlanRequest) -> Inscription:
    member = _resolve_member(db, data.member_id, data.dni)

    if not member.is_active:
        raise BusinessRuleError("Cannot assign a plan to an inactive member")

    plan = crud_plans.get_plan_by_id(db, data.plan_id)
    if plan is None:
        raise NotFoundError(f"Plan with id {data.plan_id} was not found")
    if not plan.is_active:
        raise BusinessRuleError("Cannot assign an inactive plan")

    if crud_members.get_active_inscription_by_member(db, member.id) is not None:
        raise ConflictError("Member already has an active inscription")

    if data.end_date is not None and data.end_date <= data.start_date:
        raise BusinessRuleError("end_date must be later than start_date")

    return crud_members.create_inscription(
        db,
        member_id=member.id,
        plan_id=plan.id,
        start_date=data.start_date,
        end_date=data.end_date,
    )


def apply_discount(db: Session, data: ApplyDiscountRequest) -> Discount:
    member = _resolve_member(db, data.member_id, data.dni)

    if not member.is_active:
        raise BusinessRuleError("Cannot apply a discount to an inactive member")

    return crud_members.create_discount(
        db,
        percentage=data.percentage,
        reason=data.reason,
        member_id=member.id,
        inscription_id=data.inscription_id,
    )


def deactivate_discount(db: Session, discount_id: int) -> Discount:
    discount = crud_members.get_discount_by_id(db, discount_id)
    if discount is None:
        raise NotFoundError(f"Discount with id {discount_id} was not found")
    if not discount.is_active:
        raise BusinessRuleError(f"Discount with id {discount_id} is already inactive")
    return crud_members.deactivate_discount(db, discount)


def list_plans(db: Session, is_active: Optional[bool] = None) -> list[Plan]:
    return crud_plans.get_all_plans(db, is_active=is_active)


def get_plan(db: Session, plan_id: int) -> Plan:
    plan = crud_plans.get_plan_by_id(db, plan_id)
    if plan is None:
        raise NotFoundError(f"Plan with id {plan_id} was not found")
    return plan


def create_plan(db: Session, data: PlanCreate) -> Plan:
    if crud_plans.get_plan_by_name(db, data.name):
        raise ConflictError(f"A plan named '{data.name}' already exists")
    return crud_plans.create_plan(db, data)


def _resolve_member(db: Session, member_id: Optional[int], dni: Optional[str]) -> Member:
    #OP CODE - Accepts either the internal id or the unique dni, but exactly one.
    if member_id is None and dni is None:
        raise BusinessRuleError("Provide either member_id or dni")
    if member_id is not None and dni is not None:
        raise BusinessRuleError("Provide only one of member_id or dni")

    if member_id is not None:
        return get_member(db, member_id)
    return get_member_by_dni(db, dni)

#OP CODE END
