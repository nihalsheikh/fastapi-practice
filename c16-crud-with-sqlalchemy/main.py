from fastapi import FastAPI, HTTPException, status, Request, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, Session

app = FastAPI()

DB_URL = "sqlite:///./test.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

session_local = sessionmaker(bind=engine)

Base = declarative_base()


class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    is_completed = Column(Boolean, nullable=False, default=False)


Base.metadata.create_all(bind=engine)


# Check and make a db session
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


@app.get("/", status_code=status.HTTP_200_OK)
def home(db: Session = Depends(get_db)):
    return {"msg": "DB Connection Success"}


class TodoCreate(BaseModel):
    title: str
    is_completed: bool


class TodoResponse(BaseModel):
    id: int
    title: str
    is_completed: bool


class AllTodoResponse(BaseModel):
    total: int
    message: str
    todos: list[TodoResponse]


class TodoMessageResponse(BaseModel):
    message: str
    todo: TodoResponse


# Create todo
@app.post(
    "/todos", status_code=status.HTTP_201_CREATED, response_model=TodoMessageResponse
)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    # Make a todo obj
    new_todo = Todo(title=todo.title, is_completed=todo.is_completed)

    # add to db, save and refresh db
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)

    return {"message": "Todo Created Successfully", "todo": new_todo}


# Get All Todos
@app.get("/todos", status_code=status.HTTP_200_OK, response_model=AllTodoResponse)
def get_todos(db: Session = Depends(get_db)):
    todos = db.query(Todo).all()
    return {"total": len(todos), "message": "Fetched all todos", "todos": todos}

# Get Todo
@app.get("/todos/{todo_id}", status_code=status.HTTP_200_OK, response_model=TodoMessageResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    return { "message": "Fetched your todo", "todo": todo }


# Update Todo
@app.put("/todos/{todo_id}", status_code=status.HTTP_200_OK, response_model=TodoMessageResponse)
def update_todo(todo_id: int, new_todo: TodoCreate, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    todo.title = new_todo.title
    todo.is_completed = new_todo.is_completed

    db.commit()
    db.refresh(todo)

    return { "message": "Todo updated successfully", "todo": todo }

# Delete Todo
@app.delete("/todos/{todo_id}", status_code=status.HTTP_200_OK)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    db.delete(todo)
    db.commit()

    return { "message": "Todo deleted successfully" }
