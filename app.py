import os
import json
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

# AWS S3 Configuration
S3_AWS_REGION = os.getenv("S3_AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET")
MASS_FILES = os.getenv("MASS_FILES", default="mass/")

s3_client = boto3.client("s3", region_name=S3_AWS_REGION)


class FileList(BaseModel):
    files: List[str]


class FileContent(BaseModel):
    songs: list


@app.get("/")
async def hello():
    return "Welcome to PG Choir Pyesa. A choir companion during Sunday Mass."


@app.get("/prod")
async def prod():
    return "Hello prod"


@app.get("/api/files", response_model=FileList)
async def list_files():
    """List JSON files in S3."""
    try:
        response = s3_client.list_objects_v2(
            Bucket=S3_BUCKET, Prefix=MASS_FILES
        )
        files = [
            obj["Key"].replace(MASS_FILES, "")
            for obj in response.get("Contents", [])
            if obj["Key"].endswith(".json")
        ]
        return {"files": sorted(files, reverse=True)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/files/{filename}", response_model=FileContent)
async def read_file(filename: str):
    """Read a JSON file from S3."""
    if not filename.endswith(".json"):
        raise HTTPException(
            status_code=400, detail="Only .json files are supported"
        )

    try:
        response = s3_client.get_object(
            Bucket=S3_BUCKET, Key=f"{MASS_FILES}{filename}"
        )
        file_content = response["Body"].read().decode("utf-8")
        return json.loads(file_content)
    except s3_client.exceptions.NoSuchKey:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
