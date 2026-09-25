from fastapi import FastAPI, HTTPException, status, UploadFile, File
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import shutil


app = FastAPI()

# Folder name and File Path to save files
UPLOAD_DIR = "uploads"

# check if folder exists, if not make one
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# Static File setup
# URL for file upload will look like this:
# http://127.0.0.1:8000/files/{filename}
app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="files")

# Response Models
class UploadResponse(BaseModel):
    message: str
    filename: str
    file_url: str

class GetFileResponse(BaseModel):
    message: str
    file_url: str

# Upload File Route
@app.post("/upload", status_code=status.HTTP_201_CREATED, response_model=UploadResponse)
def upload_file(file: UploadFile = File(...)):
    filename = file.filename

    if not filename:
        raise HTTPException(
            status_code=400,
            detail="File not selected/uploaded"
        )

    file_path = os.path.join(UPLOAD_DIR, filename)

    # save file to folder
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

        return {
            "message": "File uploaded successfully",
            "filename": filename,
            "file_url": f"http://127.0.0.1:8000/files/{filename}"
        }


# Get the Uploaded File URL
@app.get("/files/{filename}", status_code=status.HTTP_200_OK, response_model=GetFileResponse)
def get_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )

    return {
        "message": "Fetched the File URL",
        "file_url": f"http://127.0.0.1:8000/files{filename}"
    }

# Health check
@app.get("/", status_code=status.HTTP_200_OK)
def home():
    return {"message": "Everything is running."}
