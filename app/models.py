from datetime import datetime, date
from enum import Enum as PyEnum
from typing import Optional, List
from sqlalchemy import String, ForeignKey, Numeric, DateTime, Date, Boolean, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class RolUsuario(str, PyEnum):
    ADMIN = "ADMIN"
    GESTOR = "GESTOR"

class FrecuenciaPlan(str, PyEnum):
    MENSUAL = "MENSUAL"
    CUATRIMESTRAL = "CUATRIMESTRAL"
    ANUAL = "ANUAL"

class EstadoInscripcion(str, PyEnum):
    ACTIVA = "ACTIVA"
    SUSPENDIDA = "SUSPENDIDA"
    FINALIZADA = "FINALIZADA"

class MetodoPago(str, PyEnum):
    EFECTIVO = "EFECTIVO"
    TRANSFERENCIA = "TRANSFERENCIA"
    MERCADOPAGO = "MERCADOPAGO"

class EstadoPago(str, PyEnum):
    PENDIENTE = "PENDIENTE"
    COMPLETADO = "COMPLETADO"
    ANULADO = "ANULADO"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255),nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    rol: Mapped[RolUsuario] = mapped_column(Enum(RolUsuario), default=RolUsuario.GESTOR, nullable=False)

    #pagos_registrados: Mapped[List["Pago"]] = relationship(back_populates="usuario")

"""
class Jugador(Base):
    __tablename__ = "jugadores"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    dni: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    apellido: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    telefono: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    fecha_nacimiento: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    inscripciones: Mapped[List["Inscripcion"]] = relationship(back_populates="jugador")


class Plan(Base):
    __tablename__ = "planes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    monto_base: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    frecuencia: Mapped[FrecuenciaPlan] = mapped_column(Enum(FrecuenciaPlan), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    inscripciones: Mapped[List["Inscripcion"]] = relationship(back_populates="plan")


class Inscripcion(Base):
    __tablename__ = "inscripciones"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    jugador_id: Mapped[int] = mapped_column(ForeignKey("jugadores.id"), nullable=False)
    plan_id: Mapped[int] = mapped_column(ForeignKey("planes.id"), nullable=False)
    fecha_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_fin: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    estado: Mapped[EstadoInscripcion] = mapped_column(Enum(EstadoInscripcion), default=EstadoInscripcion.ACTIVA, nullable=False)
    motivo_baja: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    jugador: Mapped["Jugador"] = relationship(back_populates="inscripciones")
    plan: Mapped["Plan"] = relationship(back_populates="inscripciones")
    pagos: Mapped[List["Pago"]] = relationship(back_populates="inscripcion")


class Pago(Base):
    __tablename__ = "pagos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    inscripcion_id: Mapped[int] = mapped_column(ForeignKey("inscripciones.id"), nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    
    
    monto_congelado: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    fecha_emision: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    fecha_pago: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    metodo_pago: Mapped[MetodoPago] = mapped_column(Enum(MetodoPago), nullable=False)
    estado: Mapped[EstadoPago] = mapped_column(Enum(EstadoPago), default=EstadoPago.PENDIENTE, nullable=False)
    webhook_id: Mapped[Optional[str]] = mapped_column(String(255), unique=True, nullable=True, index=True)

    
    inscripcion: Mapped["Inscripcion"] = relationship(back_populates="pagos")
    usuario: Mapped["User"] = relationship(back_populates="pagos_registrados")

"""