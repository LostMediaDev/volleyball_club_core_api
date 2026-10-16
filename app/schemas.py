from pydantic import BaseModel, Field, EmailStr
from typing import Optional

#Schema for new register user 


class userCreate(BaseModel):
    name: str = Field(...,min_length=2,max_length=20)
    email: EmailStr
    password: str = Field(...,min_length=6)

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

    class config:
        from_atributes = True
    