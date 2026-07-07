from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

#class UserModel(Base):
   # __tablename__="users"
   # id = Column(Integer, primary_key=True, index=True)
   # email = Column(String, unique=True, index=True, nullable=False)
   # hashed_password = Column(String, nullable=False)

   # todos = relationship("ToDoModel", back_populates="owner")

class ToDoModel(Base):
    __tablename__ = "todos"

    id = Column(Integer, nullable=False, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    completed = Column(Boolean, default=False)

    #owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    #owner = relationship("UserModel", back_populates="todos")
