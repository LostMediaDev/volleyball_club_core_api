from typing import Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.depends import require_role
from app.database import get_db
from app.schemas import PlanCreate, PlanResponse
from app.services import service_members

#Training plan endpoints

router = APIRouter(
    prefix="/plans",
    tags=["Plans"],
)


@router.post("", response_model=PlanResponse, status_code=status.HTTP_201_CREATED)
def create_plan(
    data: PlanCreate,
    current_user=Depends(require_role("GESTOR")),
    db: Session = Depends(get_db),
):
    return service_members.create_plan(db, data)


@router.get("", response_model=list[PlanResponse])
def list_plans(
    is_active: Optional[bool] = None,
    current_user=Depends(require_role("GESTOR")),
    db: Session = Depends(get_db),
):
    return service_members.list_plans(db, is_active=is_active)


@router.get("/{plan_id}", response_model=PlanResponse)
def get_plan(
    plan_id: int,
    current_user=Depends(require_role("GESTOR")),
    db: Session = Depends(get_db),
):
    return service_members.get_plan(db, plan_id)

#OP CODE END
