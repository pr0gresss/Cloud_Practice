from pydantic import BaseModel, Field

class FeedbackCreate(BaseModel):
    content: str

class PortfolioCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    surname: str = Field(min_length=1, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class PortfolioUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=100)
    surname: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class PortfolioOut(PortfolioCreate):
    portfolioId: int

    class Config:
        from_attributes = True