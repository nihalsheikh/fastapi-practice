from fastapi import FastAPI, Depends, status, HTTPException, Header
from pydantic import BaseModel

app = FastAPI()

def common_message():
    return  { "message": "Common Message Fn Executed" }

@app.get("/", status_code=status.HTTP_200_OK)
def home(data = Depends(common_message)):
    return data

class GetUserRequest(BaseModel):
    id: int
    name: str
    age: int

class UserResponse(BaseModel):
    message: str
    user: GetUserRequest

# store users
users = []

# global fn to get user
def get_current_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(
        status_code=404,
        detail="User not found"
    )

@app.get("/users", status_code=status.HTTP_200_OK)
def get_users():
    return { "users": users }

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: GetUserRequest):
    users.append(user)
    return { "message": "User created", "user": user }

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user_profile(user_id: int, user = Depends(get_current_user)):
    return { "message": "Got user profile", "user": user }

# Token
TOKEN = "6637239c225ae5bb8daa40b98788fb108a71888219b40b3feeea9c26c104afca"

# global fn to verify token
def verify_token(token: str = Header(None)):
    if token != TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized user"
        )
    return { "message": "Authorized user" }

@app.get("/auth/user")
def get_auth_user(user = Depends(verify_token)):
    return { "message": "User is authenticated", "user": user }
