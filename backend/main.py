from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas, crud
from database import engine, Base, get_db
from fastapi import BackgroundTasks
from ai import analyze_sentiment

app = FastAPI()

Base.metadata.create_all(bind=engine)

def process_review(review_id: int, db):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()

    sentiment, score = analyze_sentiment(review.review_text)

    analytics = models.Analytics(
        review_id=review.id,
        sentiment=sentiment,
        confidence=score
    )

    db.add(analytics)

    # optional: update status
    review.status = "Completed"

    db.commit()

@app.post("/products")
def create_product(data: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, data.name, data.description)


@app.post("/reviews")
def create_review(data: schemas.ReviewCreate, db: Session = Depends(get_db)):
    return crud.create_review(db, data.product_id, data.review_text)

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return crud.get_products(db)


@app.get("/reviews")
def get_reviews(db: Session = Depends(get_db)):
    return crud.get_reviews(db)

@app.post("/submit-review")
def submit_review(data: schemas.ReviewCreate, bg: BackgroundTasks, db: Session = Depends(get_db)):
    
    review = crud.create_review(db, data.product_id, data.review_text)

    bg.add_task(process_review, review.id, db)

    return {"message": "Review submitted, processing started"}

@app.get("/analytics-summary")
def analytics_summary(db: Session = Depends(get_db)):
    return crud.get_analytics_summary(db)