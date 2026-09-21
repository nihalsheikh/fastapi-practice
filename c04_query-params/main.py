from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return { "message": "Home Route" }

@app.get("/users")
def users(name: str = None):
    return { "name": name }

@app.get("/products")
def get_product(limit: int = 10, product_name: str = None, product_id: int = None):
    return { "name": product_name, "id": product_id, "limit": limit }

@app.get("/items")
def get_items(name: str = None, price: int = 0):
    return { "name": name, "price": price }
