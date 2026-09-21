from fastapi import FastAPI, status, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    name: str

users = []

@app.get("/", status_code=status.HTTP_200_OK)
def home():
    return { "message": "Home Route" }

@app.get("/users", status_code=status.HTTP_200_OK)
def get_users():
    return { "users": users }

@app.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    users.append(user)
    return { "message": "User created", "user": user }

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: int):
    for idx, user in enumerate(users):
        if user.id == user_id:
            return { "user": user }

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return { "message": "Invalid User Id" }


class ItemRequest(BaseModel):
    id: int
    name: str
    price: int
    quantity: int

class ItemDetails(BaseModel):
    name: str
    price: int
    quantity: int

class ItemResponse(BaseModel):
    message: str
    item: ItemDetails

class ItemNotFoundException(Exception):
    def __init__(self, item: str):
        self.item = item

@app.exception_handler(ItemNotFoundException)
def item_not_found_handler(req: Request, exc: ItemNotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "status": "error",
            "message": f"Item {exc.item} not found"
        }
    )

items = []

@app.get("/items", status_code=status.HTTP_200_OK)
def get_items():
    return { "message": "Fetched Items", "item": items }

@app.post("/items", status_code=status.HTTP_201_CREATED, response_model=ItemResponse)
def create_item(item: ItemRequest):
    items.append(item)
    return { "message": "Item Created", "item": item }

@app.get("/items/{item_id}", status_code=status.HTTP_200_OK)
def get_item(item_id: int):
    for item in items:
        if item.id == item_id:
            return { "item": item }
    raise ItemNotFoundException(item_id)
