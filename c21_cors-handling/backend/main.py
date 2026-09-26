from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add the CORS origin sources
origins = [
    "http://localhost:5173"
]

# Add the CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # allow all HTTP methods [GET, PUT, POST, DELETE...]
    allow_headers=["*"]
)

@app.get("/")
def home():
    return {"msg":"CORS Enabled"}
