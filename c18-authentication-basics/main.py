from fastapi import FastAPI, Header, Depends, HTTPException, status
from pydantic import BaseModel
from datetime import datetime, timedelta, timezone
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from jose import jwt

app = FastAPI()

# DB configs
DB_URL = "sqlite:///./test-users.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread":False})

session_local = sessionmaker(bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_public = Column(Boolean, nullable=False, default=True)

Base.metadata.create_all(bind=engine)

# Get DB connection
def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

# User Schema Models
class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    password: str
    is_public: bool

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    is_public: bool

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_public: bool

class UserMessage(BaseModel):
    message: str
    user: UserResponse

class UserLoginMessage(BaseModel):
    message: str
    access_token: str


# Token Configs
SECRET_KEY = "34476d5a2bc49ed8de3afc3a99fc503d52fa35112a3ef0de3d9c3f86d6b0e2cc"

ALGORITHM = "HS256"

# Create token
def create_token(user: User):
    to_encode = {
        "sub": str(user.id),
        "email": user.email
    }

    expire_time = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode.update({"exp": expire_time})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

# Verify token
def verify_token(token: str = Header(None)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid Token"
            )

        return int(user_id)
    except (jwt.JWTError, ValueError, TypeError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or Expired Token"
        )

# Create User
@app.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserMessage)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(name=user.name, email=user.email, password=user.password, is_public=user.is_public)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created", "user": new_user}

# User Login
@app.post("/signin", status_code=status.HTTP_200_OK, response_model=UserLoginMessage)
async def signin(user: UserLogin, db: Session = Depends(get_db)):
    usr = db.query(User).filter(User.email == user.email, User.password == user.password).first()

    if not usr:
        raise HTTPException(
            status_code=401,
            detail="Invalid Email or Password"
        )

    token = create_token(usr)

    return {"message":"Login Successfull", "access_token": token}

# User Profile
@app.get("/profile", status_code=status.HTTP_200_OK, response_model=UserMessage)
def get_user(user_id: int = Depends(verify_token), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {"message": "Fetched profile details", "user": user}


# Health Check DB Route
@app.get("/db-health")
def check_db_connection(db: Session = Depends(get_db)):
    return { "message": "DB Connection Success" }
