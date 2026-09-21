from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

app = FastAPI()

class HomeResponse(BaseModel):
    mesasge: str

class User(BaseModel):
    id: int
    name: str
    age: int

class UserCreated(BaseModel):
    message: str
    user: User

users = []

@app.get("/", response_model=HomeResponse, status_code=status.HTTP_200_OK)
def home():
    return { "message": "Home Route" }

@app.post("/users", response_model=UserCreated, status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    users.append(user)
    return { "message": "User created", "user": user }

@app.get("/users", status_code=status.HTTP_200_OK)
def get_users():
    return { "users": users }

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: int):
    if user_id < 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    for idx, usr in enumerate(users):
        if usr.id == user_id:
            return { "user": usr }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User does not exist"
    )
