from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from fastapi import FastAPI, status, Depends


app = FastAPI()

# DB url
DATABASE_URL = "sqlite:///./test.db"

# connect to db
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# perform ops in the connected db
session_local = sessionmaker(bind=engine)

# Make model
Base = declarative_base()

# Model
class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, nullable=False)
    completed = Column(String)

# create table
Base.metadata.create_all(bind=engine)

# Get DB session
def get_db():
    # creating new db session
    db = session_local()
    try:
        # return API db session
        yield db
    finally:
        # after req, db session closed
        db.close()

# Home Route and check DB connection
@app.get("/", status_code=status.HTTP_200_OK)
def home(db: Session = Depends(get_db)):
    return {"message": "DB Connection Success"}
