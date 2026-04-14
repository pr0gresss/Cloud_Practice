from pydantic import BaseModel

class ArtworkCreate(BaseModel):
    portfolioId: int
    imageUrl: str
    title: str
    description: str

class ArtworkOut(ArtworkCreate):
    artworkId: int

    class Config:
        from_attributes = True