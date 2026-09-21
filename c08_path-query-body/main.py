from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    age: int
    notify: bool


users = []


@app.get("/")
def home():
    return {"message": "This is Home Route"}


@app.get("/users")
def get_users():
    return {"data": users}


@app.post("/users")
def create_user(user: User):
    users.append(user)
    return {"message": "User created", "user": user}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    for idx, usr in enumerate(users):
        if usr.id == user_id:
            return {"data": usr}


@app.put("/users/{user_id}")
def update_user(user_id: int, updated_user: User, notify: bool = False):
    for idx, usr in enumerate(users):
        if usr.id == user_id:
            users[idx] = updated_user
            if usr.notify == notify:
                usr.notify = notify
            return {"message": "Data updated", "data": users[idx]}
        return {"message": "User doesn't exist"}
    return {"message": "Error updated user"}


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for idx, usr in enumerate(users):
        if usr.id == user_id:
            users.pop(idx)
            return {"message": "User deleted"}
        return {"message": "User doesn't exist"}
    return {"message": "Error deleting user"}
