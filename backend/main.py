from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os

app = FastAPI()
# Ensure uploads folder exists
os.makedirs("uploads", exist_ok=True)


# Allow frontend (HTML/JS) to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Example route
@app.get("/")
def home():
    return {"message": "Food Sharing Backend is running!"}

# Upload food photo
@app.post("/upload/")
async def upload_food(photo: UploadFile = File(...), description: str = Form(...)):
    file_location = f"uploads/{photo.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(photo.file, buffer)
    return {"info": f"File '{photo.filename}' saved", "description": description}
