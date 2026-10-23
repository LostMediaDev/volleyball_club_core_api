from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db


from app.schemas import userCreate, userResponse, userLoginSchema, token
from app.crud import crud_user
from app.core import security
from app.core.depends import get_current_user, require_role
 

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)


@router.post("/login",response_model=token)
def try_login_user(
    user_credentials : userLoginSchema,
    db:Session = Depends(get_db)
):
    user_on = crud_user.get_user_by_email(db,user_credentials.email)

    if not user_on:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="reget"
        )

    login_user_password = user_credentials.password
    db_user_password = crud_user.get_user_hashed_password(db,user_credentials.email)

    password_verified = security.verify_password(login_user_password,db_user_password)

    if not password_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="reget"
        )
    
    

    access_token = security.create_access_token(
        data={"sub": user_on.email, "rol": user_on.rol}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/",response_model=list[userResponse])
def try_get_user(
    current_user = Depends(require_role("ADMIN")),
    db: Session = Depends(get_db)
):

    users = crud_user.get_all_users(db)
    return users

@router.post("/register",response_model=userResponse,status_code=status.HTTP_201_CREATED)
def try_register_new_user(
    user_data : userCreate,
    current_user = Depends(require_role("ADMIN")),
    db: Session = Depends(get_db)
):
    #verify if user exist
    user_exist = crud_user.get_user_by_email(db,user_data.email)

    if user_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    new_user = crud_user.create_user(db=db,user=user_data)
    
    return new_user
    