from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from config import settings

app = FastAPI()

# Origins
# origins = os.getenv("ORIGINS")
# db_url = os.getenv("DB_URL")
origins = settings.origins
db_url = settings.db_url
secret_key = settings.secret_key

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Home Route
@app.get("/")
def home():
    return {"message": "CORS Enabled. Home Route"}
