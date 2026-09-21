from fastapi import FastAPI

app = FastAPI()

# Home
@app.get("/")
def home():
    return {"status": "OK", "message": "Home Route"}

# Users
@app.get("/users")
def users():
    return {"status": "OK", "message": "This is Users Route", "users": ["Alex", "John", "Jane"]}

# Get Users
@app.get("/users/{user_id}")
async def get_users(user_id: str):
    return  { "status": "OK", "mesasge": "User Id", "user_id": user_id}
