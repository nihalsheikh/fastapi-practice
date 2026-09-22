from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

connect_db = sqlite3.connect("test.db", check_same_thread=False)

cursor = connect_db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS todos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        completed BOOLEAN DEFAULT 0
    )
""")

connect_db.commit()

@app.get("/", status_code=status.HTTP_200_OK)
def home():
    return {"message": "SQLite Connected"}
