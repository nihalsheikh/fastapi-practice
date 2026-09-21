from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Todo(BaseModel):
    id: int
    title: str
    description: str
    is_completed: bool

@app.get("/")
def home():
    return { "message": "Home Route" }

todos = []

@app.post("/todos")
def create_todo(todo: Todo):
    todos.append(todo)
    return {"message": "Todo Created successfully", "data": todo}

@app.get("/todos")
def get_todos():
    return { "all_todos": todos }

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for td in todos:
        if td.id == todo_id:
            return { "my_todo":"Got your todo", "data":td }
    return { "message": "Todo doesn't exist" }

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, new_todo: Todo):
    for idx, td in enumerate(todos):
        if td.id == todo_id:
            todos[idx] = new_todo
            return { "message": "Todo updated successfully", "data": new_todo }
        else:
            return { "message": "Todo doesn't exist" }
    return { "message": "Error updating todo" }

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for idx, td in enumerate(todos):
        if td.id == todo_id:
            todos.pop(idx)
            return { "message": "Todo deleted successfully", "data": todos }
        else:
            return { "message": "Todo doesn't exist"  }
    return { "message": "Error deleting todo" }
