from datetime import date
from typing import Optional

from sqlalchemy.orm import Session

from app.models import Discount, Inscription, Member
from app.schemas import MemberCreate, MemberUpdate

#Data access layer for members, inscriptions and discounts.

def get_member_by_id(db: Session, member_id: int) -> Optional[Member]:
    return db.query(Member).filter(Member.id == member_id).first()


def get_member_by_dni(db: Session, dni: str) -> Optional[Member]:
    return db.query(Member).filter(Member.dni == dni).first()


def get_member_by_email(db: Session, email: str) -> Optional[Member]:
    return db.query(Member).filter(Member.email == email).first()


def get_all_members(db: Session, is_active: Optional[bool] = None) -> list[Member]:
    this_query = db.query(Member)
    if is_active is not None:
        this_query = query.filter(Member.is_active == is_active)
    return this_query.all()


def create_member(db: Session, data: MemberCreate) -> Member:
    db_member = Member(
        dni=data.dni,
        nombre=data.nombre,
        apellido=data.apellido,
        email=data.email,
        telefono=data.telefono,
        fecha_nacimiento=data.fecha_nacimiento,
    )
    return _save(db, db_member)


def update_member(db: Session, member: Member, data: MemberUpdate) -> Member:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(member, field, value)
    return _save(db, member)


def soft_delete_member(db: Session, member: Member) -> Member:
    member.is_active = False
    return _save(db, member)


def get_active_inscription_by_member(db: Session, member_id: int) -> Optional[Inscription]:
    return (
        db.query(Inscription)
        .filter(Inscription.member_id == member_id, Inscription.status == "ACTIVA")
        .first()
    )


def create_inscription(
    db: Session,
    member_id: int,
    plan_id: int,
    start_date: date,
    end_date: Optional[date] = None,
) -> Inscription:
    db_inscription = Inscription(
        member_id=member_id,
        plan_id=plan_id,
        start_date=start_date,
        end_date=end_date,
    )
    return _save(db, db_inscription)


def create_discount(
    db: Session,
    percentage,
    reason: Optional[str] = None,
    member_id: Optional[int] = None,
    inscription_id: Optional[int] = None,
) -> Discount:
    db_discount = Discount(
        member_id=member_id,
        inscription_id=inscription_id,
        percentage=percentage,
        reason=reason,
    )
    return _save(db, db_discount)


def get_discount_by_id(db: Session, discount_id: int) -> Optional[Discount]:
    return db.query(Discount).filter(Discount.id == discount_id).first()


def deactivate_discount(db: Session, discount: Discount) -> Discount:
    discount.is_active = False
    return _save(db, discount)


def get_active_discounts_by_member(db: Session, member_id: int) -> list[Discount]:
    return (
        db.query(Discount)
        .filter(Discount.member_id == member_id, Discount.is_active.is_(True))
        .all()
    )


def _save(db: Session, instance):
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance

#OP CODE END
