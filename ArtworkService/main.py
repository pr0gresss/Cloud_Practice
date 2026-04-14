from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from contextlib import asynccontextmanager
import uuid
import os
import logging

from models import Artwork
from schemas import ArtworkCreate, ArtworkOut
from db import get_db, engine, Base

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("artwork-service")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized")
    yield
    logger.info("Service stopped")


app = FastAPI(title="Artwork Service", lifespan=lifespan)


# UPLOAD IMAGE
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    filename = f"{uuid.uuid4()}.jpg"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as f:
        f.write(await file.read())

    logger.info(f"File uploaded: {filename}")
    return {"url": path}


# CREATE ARTWORK
@app.post("/artworks", response_model=ArtworkOut)
def create_artwork(data: ArtworkCreate, db: Session = Depends(get_db)):
    obj = Artwork(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)

    logger.info(f"Created artwork {obj.artworkId}")
    return obj


# GET ALL
@app.get("/artworks")
def get_all_artworks(db: Session = Depends(get_db)):
    res = db.execute(select(Artwork))
    return res.scalars().all()


# GET BY ID
@app.get("/artworks/{id}", response_model=ArtworkOut)
def get_artwork(id: int, db: Session = Depends(get_db)):
    res = db.execute(select(Artwork).where(Artwork.artworkId == id))
    obj = res.scalar_one_or_none()

    if not obj:
        raise HTTPException(status_code=404, detail="Artwork not found")

    return obj


# UPDATE
@app.put("/artworks/{id}", response_model=ArtworkOut)
def update_artwork(id: int, data: ArtworkCreate, db: Session = Depends(get_db)):
    res = db.execute(select(Artwork).where(Artwork.artworkId == id))
    obj = res.scalar_one_or_none()

    if not obj:
        raise HTTPException(status_code=404, detail="Artwork not found")

    for key, value in data.dict().items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)

    logger.info(f"Updated artwork {id}")
    return obj


# DELETE
@app.delete("/artworks/{id}")
def delete_artwork(id: int, db: Session = Depends(get_db)):
    res = db.execute(select(Artwork).where(Artwork.artworkId == id))
    obj = res.scalar_one_or_none()

    if not obj:
        raise HTTPException(status_code=404, detail="Artwork not found")

    db.delete(obj)
    db.commit()

    logger.info(f"Deleted artwork {id}")
    return {"message": "Deleted successfully"}