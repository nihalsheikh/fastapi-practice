from fastapi import FastAPI

app = FastAPI()

# Home
@app.get("/")
def home():
    return {"status": "OK", "message": "Home Route"}

# About
@app.get("/about")
def about():
    return {"status": "OK", "message": "This is About Route"}

# Contact
@app.get("/contact")
def contact():
    return {"status": "OK", "message": "This is Contact Route"}

# Users
@app.get("/users")
def users():
    return {"status": "OK", "message": "This is Users Route", "users": ["Alex", "John", "Jane"]}
