from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from contextlib import asynccontextmanager
import logging

from service_bus import send_feedback_message
from models import Portfolio
from schemas import FeedbackCreate, PortfolioCreate, PortfolioUpdate, PortfolioOut
from db import get_db, engine, Base

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("portfolio-service")


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized")
    yield
    logger.info("Service stopped")


app = FastAPI(title="Portfolio Service", lifespan=lifespan)


# CREATE
@app.post("/portfolios", response_model=PortfolioOut)
def create_portfolio(data: PortfolioCreate, db: Session = Depends(get_db)):
    portfolio = Portfolio(**data.dict())
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)

    logger.info(f"Created portfolio {portfolio.portfolioId}")
    return portfolio


# GET BY ID
@app.get("/portfolios/{id}", response_model=PortfolioOut)
def get_portfolio(id: int, db: Session = Depends(get_db)):
    result = db.execute(select(Portfolio).where(Portfolio.portfolioId == id))
    portfolio = result.scalar_one_or_none()

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    return portfolio


# GET ALL
@app.get("/portfolios")
def get_all_portfolios(db: Session = Depends(get_db)):
    result = db.execute(select(Portfolio))
    return result.scalars().all()


# UPDATE
@app.put("/portfolios/{id}", response_model=PortfolioOut)
def update_portfolio(id: int, data: PortfolioUpdate, db: Session = Depends(get_db)):
    result = db.execute(select(Portfolio).where(Portfolio.portfolioId == id))
    portfolio = result.scalar_one_or_none()

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(portfolio, key, value)

    db.commit()
    db.refresh(portfolio)

    logger.info(f"Updated portfolio {id}")
    return portfolio


# DELETE
@app.delete("/portfolios/{id}")
def delete_portfolio(id: int, db: Session = Depends(get_db)):
    result = db.execute(select(Portfolio).where(Portfolio.portfolioId == id))
    portfolio = result.scalar_one_or_none()

    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    db.delete(portfolio)
    db.commit()

    logger.info(f"Deleted portfolio {id}")
    return {"message": "Deleted successfully"}

@app.post("/portfolios/{id}/feedback")
def send_feedback(id: int, data: FeedbackCreate):

    payload = {
        "portfolioId": id,
        "content": data.content
    }

    send_feedback_message(payload)

    return {
        "message": "Feedback queued"
    }