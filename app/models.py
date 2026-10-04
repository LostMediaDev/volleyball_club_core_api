from sqlalchemy import Column,Integer,String,Float,Boolean
from app.database import Base

class userModel(Base):
    __tablename__ = "users"

    id= Column(Integer, primary_key= True, index=True)
    user_name= Column(String, nullable=False)



