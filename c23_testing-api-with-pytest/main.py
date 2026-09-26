from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Home Route"}


@app.get("/add")
def add(a: int = 0, b: int = 0):
    return {"result": a + b}


class User(BaseModel):
    id: int
    name: str
    age: int


class UpdateUser(BaseModel):
    name: str
    age: int


class CreateResponse(BaseModel):
    message: str
    user: User


class UpdateResponse(BaseModel):
    message: str
    user: UpdateUser


class DeleteResponse(BaseModel):
    message: str
    users: list[User]


class UserListResponse(BaseModel):
    message: str
    users: list[User]


class UserResponse(BaseModel):
    message: str
    user: User


users = []


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=CreateResponse)
def create_user(user: User):
    users.append(user)

    return {"message": "User added successfully", "user": user}


@app.get("/users", status_code=status.HTTP_200_OK, response_model=UserListResponse)
def get_users():
    return {"message": "Fetched all users", "users": users}


@app.get(
    "/users/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse
)
def get_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return {"message": "User details fetched", "user": user}


@app.put(
    "/users/{user_id}", status_code=status.HTTP_200_OK, response_model=UpdateResponse
)
def update_user(user_id: int, user: UpdateUser):
    for idx, usr in enumerate(users):
        if usr.id == user_id:
            users[idx] = usr

            return {"message": "User updated successfully", "user": user}

    raise HTTPException(status_code=404, detail="User not found")


@app.delete(
    "/users/{user_id}", status_code=status.HTTP_200_OK, response_model=DeleteResponse
)
def delete_user(user_id: int):
    for idx, usr in enumerate(users):
        if usr.id == user_id:
            users.pop(idx)

            return {"message": "User deleted successfully", "users": users}

    raise HTTPException(status_code=404, detail="User not found")
