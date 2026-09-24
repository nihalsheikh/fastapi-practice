from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timezone, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import Session, sessionmaker, declarative_base
from jose import jwt, JWTError
from pydantic import BaseModel
from passlib.context import CryptContext

app = FastAPI()

# DB Config
DB_URL = "sqlite:///./oauth-test.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread":False})

session_local = sessionmaker(bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, index=True, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

# JWT Config
SECRET_KEY = "592866987d85352442200754c49fe42d8774122fbebcb3d08d22ca096da49bf4"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OAuth2 Setup
oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

# Password Hashing Setup
pswd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

# Hash Password
def hash_password(user_password: str):
    return pswd_context.hash(user_password)

# Verify Password
def verify_password(user_password: str, hash_password: str):
    return pswd_context.verify(user_password, hash_password)

# create token
def create_token(user: User):
    to_encode = {
        "sub": str(user.id),
        "email": user.email
    }

    expire_time = datetime.now(timezone.utc) + timedelta(minutes=30)

    to_encode.update({
        "exp": expire_time
    })

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

# verify token
def verify_token(token: str = Depends(oauth2_schema)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid Token"
            )

        return int(user_id)
    except (JWTError, ValueError, TypeError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or Expired token"
        )

# User and Response Schema
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserDetails(BaseModel):
    id: int
    name: str
    email: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    message: str
    user: UserDetails

class LoginResponse(BaseModel):
    message: str
    access_token: str
    token_type: str

# User Signup
@app.post("/signup", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    user_exist = db.query(User).filter(User.email == user.email).first()

    if user_exist:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    hashed_password = pswd_context.hash(user.password)
    new_user = User(name=user.name, email=user.email, password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message":"User created successfully", "user": new_user}

# User Login
@app.post("/login", status_code=status.HTTP_200_OK, response_model=LoginResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usr = db.query(User).filter(User.email == form_data.username).first()

    if not usr or not verify_password(form_data.password, usr.password):
        raise HTTPException(
            status_code=400,
            detail="Invalid Email or Password"
        )

    token = create_token(usr)
    return {"message": "Login successful", "access_token": token, "token_type": "bearer"}

# Protected Route check
@app.get("/profile", status_code=status.HTTP_200_OK, response_model=UserResponse)
def profile(user_id: int = Depends(verify_token), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {"message": "Protected Route accessed. Profile Details fetched", "user": user}
