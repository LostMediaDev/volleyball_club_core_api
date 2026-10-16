from fastapi import FastAPI

from app.database import engine, Base
from app.crud import crud_user 
from app.routers import user

from app.models import User


app = FastAPI(
    title="Voley managment in FastApi",
    version="1.0.0",
    description="Un gestionador de cuentas de voley, con procesos de suscripcion y pago"
)

app.include_router(user.router, prefix="/api/v1")

@app.get("/")
def root():
    return {"Mensaje":"Todo funcionando!"}
