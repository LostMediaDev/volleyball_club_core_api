from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.database import engine, Base
from app.crud import crud_user 
from app.routers import members_management, payments, plans, user

from app.models import User

#domain errors raised by the service layer
from app.services.service_members import ServiceError


app = FastAPI(
    title="Voley managment in FastApi",
    version="1.0.0",
    description="Un gestionador de cuentas de voley, con procesos de suscripcion y pago"
)

app.include_router(user.router, prefix="/api/v1")


app.include_router(members_management.router, prefix="/api/v1")
app.include_router(plans.router, prefix="/api/v1")
app.include_router(payments.router, prefix="/api/v1")


@app.exception_handler(ServiceError)
async def service_error_handler(request: Request, exc: ServiceError):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


@app.get("/")
def root():
    return {"Mensaje":"Todo funcionando!"}
