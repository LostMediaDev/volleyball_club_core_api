from typing import Optional

from sqlalchemy.orm import Session

from app.models import Plan
from app.schemas import PlanCreate

#CRUD for plan's enviroment

def get_plan_by_id(db: Session, plan_id: int) -> Optional[Plan]:
    return db.query(Plan).filter(Plan.id == plan_id).first()


def get_plan_by_name(db: Session, name: str) -> Optional[Plan]:
    return db.query(Plan).filter(Plan.name == name).first()


def get_all_plans(db: Session, is_active: Optional[bool] = None) -> list[Plan]:
    query = db.query(Plan)
    if is_active is not None:
        query = query.filter(Plan.is_active == is_active)
    return query.all()


def create_plan(db: Session, data: PlanCreate) -> Plan:
    db_plan = Plan(
        name=data.name,
        base_amount=data.base_amount,
        frequency=data.frequency,
        discount_percentage=data.discount_percentage,
        is_active=data.is_active,
    )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan
