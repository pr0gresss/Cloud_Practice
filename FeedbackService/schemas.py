from pydantic import BaseModel

class FeedbackCreate(BaseModel):
    portfolioId: int
    content: str

class FeedbackOut(FeedbackCreate):
    feedbackId: int

    class Config:
        from_attributes = True