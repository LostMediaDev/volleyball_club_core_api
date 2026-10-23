from passlib.context import CryptContext
from datetime import datetime,timedelta
import jwt
import os

SECRET_KEY = os.getenv("SECRET_KEY","nothing_here_dude")
ALGORITHM = os.getenv("ALGORITHM","HS256")


pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_password_hash(password:str) -> str:
    #Encrypt and return the hash.
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    #Compare both hashed password.
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


