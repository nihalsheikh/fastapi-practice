from fastapi import FastAPI, status, HTTPException
import requests

app = FastAPI()

@app.get("/")
def home():
    return {"msg": "Home"}

# All Posts
@app.get("/posts", status_code=status.HTTP_200_OK)
def get_posts():
    url = "https://jsonplaceholder.typicode.com/posts"
    res = requests.get(url)
    posts = res.json()
    return {"message":"Fetched all Posts", "posts": posts}

# Single Post
@app.get("/posts/{post_id}")
def get_post(post_id: int):
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"

    res = requests.get(url)
    if res.status_code != 200:
        raise HTTPException(status_code=404, detail="Post not found")

    post = res.json()
    return {"message": "Fetched post details", "post": post}

# Basic Code with Requests (no fastapi)
# response = requests.get("https://jsonplaceholder.typicode.com/posts")
# data = response.json()
# print(data)
