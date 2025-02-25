import os
import json
from pathlib import Path
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import boto3

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
FILES_FROM = os.getenv("FILES_FROM", "S3")  # Default to S3 if not specified
S3_AWS_REGION = os.getenv("S3_AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET")
MASS_FILES = os.getenv("MASS_FILES", default="mass/")
LOCAL_FILES_PATH = os.getenv("LOCAL_FILES_PATH", default="files/")

# Initialize S3 client only if needed
s3_client = boto3.client("s3", region_name=S3_AWS_REGION) if FILES_FROM == "S3" else None


class FileList(BaseModel):
    files: List[str]


class FileContent(BaseModel):
    songs: list


@app.get("/")
async def hello():
    return "Welcome to PG Choir Pyesa. A choir companion during Sunday Mass."


@app.get("/api/files", response_model=FileList)
async def list_files():
    """List JSON files from configured source."""
    try:
        if FILES_FROM == "S3":
            response = s3_client.list_objects_v2(
                Bucket=S3_BUCKET, Prefix=MASS_FILES
            )
            files = [
                obj["Key"].replace(MASS_FILES, "")
                for obj in response.get("Contents", [])
                if obj["Key"].endswith(".json")
            ]
        else:  # FILES_FROM == "FS"
            files_path = Path(LOCAL_FILES_PATH) / Path(MASS_FILES)
            files = [
                f.name for f in files_path.glob("*.json")
                if f.is_file()
            ]

        return {"files": sorted(files, reverse=True)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/files/{filename}", response_model=FileContent)
async def read_file(filename: str):
    """Read a JSON file from configured source."""
    if not filename.endswith(".json"):
        raise HTTPException(
            status_code=400, detail="Only .json files are supported"
        )

    try:
        if FILES_FROM == "S3":
            response = s3_client.get_object(
                Bucket=S3_BUCKET, Key=f"{MASS_FILES}{filename}"
            )
            file_content = response["Body"].read().decode("utf-8")
        else:  # FILES_FROM == "FS"
            file_path = Path(LOCAL_FILES_PATH) / Path(MASS_FILES) / filename
            if not file_path.exists():
                raise HTTPException(status_code=404, detail="File not found")
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()

        return json.loads(file_content)
    except s3_client.exceptions.NoSuchKey:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
