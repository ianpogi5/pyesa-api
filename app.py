from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
from pydantic import BaseModel
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory to store and read text files
FILES_DIR = os.path.join(os.path.dirname(__file__), 'files')
os.makedirs(FILES_DIR, exist_ok=True)

class FileList(BaseModel):
    files: List[str]

class FileContent(BaseModel):
    songs: list

@app.get("/api/files", response_model=FileList)
async def list_files():
    try:
        files = [f for f in os.listdir(FILES_DIR) if f.endswith('.json')]
        return {"files": sorted(files, reverse=True)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/files/{filename}", response_model=FileContent)
async def read_file(filename: str):
    if not filename.endswith('.json'):
        raise HTTPException(status_code=400, detail="Only .json files are supported")

    file_path = os.path.join(FILES_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))