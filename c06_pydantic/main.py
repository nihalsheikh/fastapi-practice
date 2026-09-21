from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    name: str
    age: int
    email: str

class Address(BaseModel):
    city: str
    pincode: int

class Citizen(BaseModel):
    person: User
    address: Address

@app.get("/")
def home():
    return { "message": "Home Route" }

@app.post("/create_user")
def create_user(user: User):
    return {
        "message": "User created successfully",
        "data": user
    }

@app.post("/create_citizen")
def create_citizen(person: Citizen):
    return {
        "message": "Added Citizen successfully",
        "citizen": person
    }
