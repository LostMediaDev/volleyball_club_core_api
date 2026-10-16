from sqlalchemy.orm import Session

from app.models import User
from app.schemas import userCreate

from app.core.security import get_password_hash, verify_password

def get_user_by_email(db:Session,email:str):

    return db.query(User).filter(User.email == email).first()

def create_user(db:Session,user:userCreate):
    
    #print("*************************************************************AQUI",user.password)
    hashed_password = get_password_hash(user.password)

    #Create new user by User
    db_user = User(
        email = user.email,
        name = user.name,
        password = hashed_password
    )

    #add and refresh database for users
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

def get_user_hashed_password(db:Session,email:str):

    user = db.query(User).filter(User.email == email).first()

    return user.password

def get_all_users(db:Session):
    return db.query(User).all()