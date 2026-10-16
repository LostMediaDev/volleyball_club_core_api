from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
import jwt
from app.database import get_db
from app.core.security import SECRET_KEY, ALGORITHM, oauth2_scheme
from app.crud import crud_user

# 1. El decodificador base
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
        
    user = crud_user.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user

# 2. El generador dinámico de roles
def require_role(required_role: str):
    def role_verifier(current_user = Depends(get_current_user)):
        if current_user.rol != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado. Se requiere el rol: {required_role}"
            )
        return current_user
    return role_verifier