from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    id: int
    name: str
    age: int
    email: str
    password: str

class UserResponse(BaseModel):
    name: str
    age: int
    email: str


users = []


@app.get("/")
def home():
    return {"message": "Home Route"}


@app.get("/users", response_model=UserResponse)
def get_users():
    return {
        "id": 1,
        "name": "John",
        "age": 25,
        "email": "jdoe@gmail.com"
    }


@app.post("/users")
def create_user(user: User):
    users.append(user)
    return { "message": "User created" }


@app.get("/users/{user_id}")
def get_user(user_id: int):
    for idx, user in users:
        if user.id == user_id:
            return {"user": user}
    return {"message": "User not found"}


@app.put("/users/{user_id}")
def get_user(user_id: int, new_user: User):
    for idx, user in users:
        if user.id == user_id:
            users[idx] = new_user
            return {"message": "User updated", "user": user}
    return {"message": "User not found"}
