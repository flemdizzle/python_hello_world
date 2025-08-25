import logging
from typing import List, Annotated
from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from connect_db import Base, engine, get_db

class TodoCreate(BaseModel):
    text: str
    complete: bool

class TodoResponse(BaseModel):
    id: int
    text: str
    complete: bool

    class Config:
        from_attributes = True

class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    complete = Column(Boolean, index=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL, e.g. ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    body = await request.body()  # Ensure body can be read
    logging.info(f"Request: {request.method} {request.url} {body}")
    response = await call_next(request)
    logging.info(f"Response status: {response.status_code}")
    return response

@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)

SessionDep = Annotated[Session, Depends(get_db)]

# DefineSessionDep = Annotated[Session, Depends(get_db)]

# Define API endpoints for CRUD operations
@app.post("/todos/", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: SessionDep):
    new_todo = Todo(**todo.model_dump())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@app.get("/todos/", response_model=List[TodoResponse])
def read_todos(db: SessionDep):
    return db.query(Todo).all()

@app.get("/todos/{todo_id}", response_model=TodoResponse)
def read_todo(todo_id: int, db: SessionDep):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoCreate, db: SessionDep):
    existing_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if existing_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    existing_todo.title = todo.title
    existing_todo.author = todo.author
    db.commit()
    db.refresh(existing_todo)
    return existing_todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: SessionDep):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"} # API endpoints for CRUD operations
@app.post("/todos/", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: SessionDep):
    new_todo = Todo(**todo.model_dump())
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

@app.get("/todos/", response_model=List[TodoResponse])
def read_todos(db: SessionDep):
    return db.query(Todo).all()

@app.get("/todos/{todo_id}", response_model=TodoResponse)
def read_todo(todo_id: int, db: SessionDep):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo: TodoCreate, db: SessionDep):
    existing_todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if existing_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    existing_todo.title = todo.title
    existing_todo.author = todo.author
    db.commit()
    db.refresh(existing_todo)
    return existing_todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: SessionDep):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted successfully"}