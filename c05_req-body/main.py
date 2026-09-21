from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    age: int
    email: str

@app.get("/")
def home():
    return { "message": "Home Route" }

@app.post("/register")
async def register(user:User):
    return {
        "message": "User created successfully",
        "user": user
    }
