from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models
import schemas
import security
from database import engine, SessionLocal

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            
    allow_credentials=True,
    allow_methods=["*"],             
    allow_headers=["*"],             
)

models.Base.metadata.create_all(bind=engine)

class ToDo(BaseModel):
    title: str
    completed: bool = False

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return({"message": "Hello World"})

@app.post("/todos")
async def create_todo(todo: ToDo, db: Session = Depends(get_db)):
    db_todo = models.ToDoModel(title=todo.title, completed=todo.completed )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.get("/todos")
async def get_todo( db: Session = Depends(get_db)):
    todos = db.query(models.ToDoModel).all()
    return todos

@app.get("/todos/{id}")
async def get_todoid(id: int, db: Session = Depends(get_db)):

    todoitem = db.query(models.ToDoModel).filter(models.ToDoModel.id == id).first()

    if not todoitem:
        raise HTTPException(status_code=404, detail=f"Task with {id} not found")

    return todoitem

@app.put("/todos/{id}")
async def update_todo(id: int, completed: bool, title: str = None, db: Session = Depends(get_db)):
    todo = db.query(models.ToDoModel).filter(models.ToDoModel.id == id).first()

    if not todo:
        raise HTTPException(status_code=404, detail=f"todo {id} not found")

    todo.completed = completed

    if title is not None:
        todo.title = title
    
    db.commit()
    db.refresh(todo)
    return todo

@app.delete("/todos/{id}")
async  def del_todo(id: int, db: Session = Depends(get_db)):
    tododelete = db.query(models.ToDoModel).filter(models.ToDoModel.id == id).first()

    if not tododelete:
        raise HTTPException(status_code=404, detail=f"todo {id} not found")

    db.delete(tododelete)
    db.commit()
    return{"detail": f"Successfully deleted task {id}"}
    
@app.post("/users", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    db_user = db.query(models.UserModel).filter(models.UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    hashed_pass = security.hash_password(user.password)

    new_user = models.UserModel(email=user.email, hashed_password=hashed_pass)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user