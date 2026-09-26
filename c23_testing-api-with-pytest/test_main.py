from fastapi.testclient import TestClient
from main import app

# Client Instance to check app endpoints
client = TestClient(app)


# Test Home EP
def test_home():
    res = client.get("/")

    # Check the Status code
    assert res.status_code == 200

    # Check the Response
    assert res.json() == {"message": "Home Route"}


# Test Add EP with Default values and Query Params
def test_add():
    res = client.get("/add")

    assert res.status_code == 200
    assert res.json() == {"result": 0}

    # Another test
    res_with_params = client.get("/add?a=5&b=4")
    assert res_with_params.status_code == 200
    assert res_with_params.json() == {"result": 9}


# Test User creation
def test_create_user():
    user = {"id": 1, "name": "John Doe", "age": 25}
    res = client.post("/users", json=user)

    assert res.status_code == 201
    assert res.json() == {"message": "User added successfully", "user": user}

# Test User Update
def test_update_user():
    user_id: int = 1
    user = {"name": "John Watson", "age": 24}

    res = client.put(f"/users/{user_id}", json=user)

    assert res.status_code == 200
    assert res.json() == {"message": "User updated successfully", "user": user}

# Test Delete user
def test_delete_user():
    user = {"id": 2, "name": "John Doe", "age": 25}
    client.post("/users", json=user)

    user_id: int = 2

    res = client.delete(f"/users/{user_id}")

    assert res.status_code == 200
    assert res.json()["message"] == "User deleted successfully"

# Test Get all users
def test_get_users():
    res = client.get("/users")

    assert res.status_code == 200
    assert  res.json()["message"] == "Fetched all users"


# Test get a user
def test_get_user():
    user = {"id": 3000, "name": "Tony Stark", "age": 30}
    client.post("/users", json=user)

    user_id: int = 3000
    res = client.get(f"/users/{user_id}")

    assert res.status_code == 200
    assert res.json() == {"message": "User details fetched", "user": user}
