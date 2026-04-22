from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from contextlib import asynccontextmanager
import logging
import time
import threading
from consumer import start_consumer

from models import Feedback
from schemas import FeedbackCreate, FeedbackOut
from db import get_db, engine, Base

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("feedback-service")


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized")

    thread = threading.Thread(target=start_consumer, daemon=True)
    thread.start()

    logger.info("Consumer started")
    yield
    logger.info("Service stopped")


app = FastAPI(title="Feedback Service", lifespan=lifespan)


# CREATE FEEDBACK
@app.post("/feedbacks", response_model=FeedbackOut)
def create_feedback(data: FeedbackCreate, db: Session = Depends(get_db)):
    obj = Feedback(**data.dict())

    db.add(obj)
    db.commit()
    db.refresh(obj)

    logger.info(f"Created feedback {obj.feedbackId}")

    # EVENT: Publish to Kafka/RabbitMQ here
    # Example:
    # publisher.publish("feedback_created", obj.dict())

    # RETRY PLACEHOLDER (pseudo)
    # for attempt in range(3):
    #     try:
    #         publish_event()
    #         break
    #     except Exception:
    #         time.sleep(0.2)

    return obj


# GET ALL FEEDBACKS
@app.get("/feedbacks")
def get_all_feedbacks(db: Session = Depends(get_db)):
    res = db.execute(select(Feedback))
    return res.scalars().all()


# GET BY ID
@app.get("/feedbacks/{id}", response_model=FeedbackOut)
def get_feedback(id: int, db: Session = Depends(get_db)):
    res = db.execute(select(Feedback).where(Feedback.feedbackId == id))
    obj = res.scalar_one_or_none()

    if not obj:
        raise HTTPException(status_code=404, detail="Feedback not found")

    return obj


# DELETE
@app.delete("/feedbacks/{id}")
def delete_feedback(id: int, db: Session = Depends(get_db)):
    res = db.execute(select(Feedback).where(Feedback.feedbackId == id))
    obj = res.scalar_one_or_none()

    if not obj:
        raise HTTPException(status_code=404, detail="Feedback not found")

    db.delete(obj)
    db.commit()

    logger.info(f"Deleted feedback {id}")
    return {"message": "Deleted successfully"}