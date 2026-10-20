from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

from app.models import FrecuenciaPlan, EstadoInscripcion, MetodoPago, EstadoPago

#Schema for new register user 


class userCreate(BaseModel):
    name: str = Field(...,min_length=2,max_length=20)
    email: EmailStr
    password: str = Field(...,min_length=6)
    rol: str

class userLoginSchema(BaseModel):
    email: EmailStr
    password: str

class userUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class userResponse(BaseModel):
    id:int
    name:str
    email:EmailStr
    rol:str

    class config:
        from_atributes = True

class token(BaseModel):
    access_token: str
    token_type: str


#OP CODE START
#OP CODE - Schemas for the member management domain (Pydantic v2, ORM mode).

class MemberCreate(BaseModel):
    dni: str = Field(..., min_length=5, max_length=20)
    nombre: str = Field(..., min_length=2, max_length=100)
    apellido: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    telefono: Optional[str] = Field(default=None, max_length=30)
    fecha_nacimiento: Optional[date] = None


class MemberUpdate(BaseModel):
    nombre: Optional[str] = Field(default=None, min_length=2, max_length=100)
    apellido: Optional[str] = Field(default=None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(default=None, max_length=30)
    fecha_nacimiento: Optional[date] = None


class MemberResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    dni: str
    nombre: str
    apellido: str
    email: EmailStr
    telefono: Optional[str]
    fecha_nacimiento: Optional[date]
    is_active: bool
    created_at: datetime


class PlanCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    base_amount: Decimal = Field(..., gt=0)
    frequency: FrecuenciaPlan
    discount_percentage: Decimal = Field(default=0, ge=0, le=100)
    is_active: bool = True


class PlanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    base_amount: Decimal
    frequency: FrecuenciaPlan
    discount_percentage: Decimal
    is_active: bool
    created_at: datetime


class AssignPlanRequest(BaseModel):
    member_id: Optional[int] = None
    dni: Optional[str] = None
    plan_id: int
    start_date: date
    end_date: Optional[date] = None


class InscriptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    member_id: int
    plan_id: int
    start_date: date
    end_date: Optional[date]
    status: EstadoInscripcion
    created_at: datetime


class ApplyDiscountRequest(BaseModel):
    member_id: Optional[int] = None
    dni: Optional[str] = None
    inscription_id: Optional[int] = None
    percentage: Decimal = Field(..., gt=0, le=100)
    reason: Optional[str] = Field(default=None, max_length=255)


class DiscountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    member_id: Optional[int]
    inscription_id: Optional[int]
    percentage: Decimal
    reason: Optional[str]
    is_active: bool
    created_at: datetime


#OP CODE START
#OP CODE - Schemas for the payment (cobros) domain.

class PaymentCreate(BaseModel):
    member_id: Optional[int] = None
    dni: Optional[str] = None
    method: MetodoPago
    payment_date: Optional[date] = None
    due_date: Optional[date] = None
    notes: Optional[str] = Field(default=None, max_length=255)


class PaymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    member_id: int
    inscription_id: int
    amount: Decimal
    discount_percentage_applied: Decimal
    method: MetodoPago
    payment_date: date
    due_date: date
    status: EstadoPago
    notes: Optional[str]
    registered_by_id: int
    registered_at: datetime
    updated_by_id: Optional[int]
    updated_at: Optional[datetime]


class PaymentAdminUpdate(BaseModel):
    amount: Optional[Decimal] = Field(default=None, gt=0)
    method: Optional[MetodoPago] = None
    payment_date: Optional[date] = None
    due_date: Optional[date] = None
    status: Optional[EstadoPago] = None
    notes: Optional[str] = Field(default=None, max_length=255)


class BillingPeriod(BaseModel):
    due_date: date
    amount: Decimal
    days_overdue: int


class BillingQuoteResponse(BaseModel):
    member_id: int
    dni: str
    inscription_id: int
    plan_id: int
    plan_name: str
    frequency: FrecuenciaPlan
    base_amount: Decimal
    discount_percentage: Decimal
    amount_due: Decimal
    total_due: Decimal
    next_due_date: Optional[date]
    status: str
    days_overdue: int
    unpaid_periods: list[BillingPeriod]

#OP CODE END