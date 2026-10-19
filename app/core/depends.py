from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer,HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import jwt
from app.database import get_db
from app.core.security import SECRET_KEY, ALGORITHM
from app.crud import crud_user

#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/user/login")

security_scheme = HTTPBearer()

# Token Decodefier.
def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
        db: Session = Depends(get_db)
        ):
    #Type credentials for use.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    #Verify if the user gmail on token it's already on DB.
    token = credentials.credentials
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

# Dinamyc Role Generator for endpoints Depends.
def require_role(required_role: str):

    def role_verifier(current_user = Depends(get_current_user)):
        #If the user has "ADMIN" Role, can access in all endpoints
        if current_user.rol == "ADMIN":
            return current_user
        elif current_user.rol != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado. Se requiere el rol: {required_role}"
            )
        return current_user
    return role_verifier