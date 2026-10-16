from passlib.context import CryptContext
from datetime import datetime,timedelta
import jwt

SECRET_KEY = "a_super_ultra_duper_hyper_secret_key"  # Idealmente va en un archivo .env
ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_password_hash(password:str) -> str:
    #Encrypt and return the hash
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    #Compare both hashed password. 
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    """Crea un token JWT con expiración."""
    to_encode = data.copy()
    # Definimos que el token expire en 30 minutos por seguridad
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    
    # Firmamos el token con nuestra clave secreta
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


