from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    description: str

class ReviewCreate(BaseModel):
    product_id: int
    review_text: str