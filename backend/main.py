from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas, crud
from database import engine, Base, get_db
from fastapi import BackgroundTasks
from ai import analyze_text
from logger import logger

app = FastAPI()

Base.metadata.create_all(bind=engine)


def process_review(review_id: int, db):
    try:
        logger.info(f"Processing review ID: {review_id}")

        review = db.query(models.Review).filter(models.Review.id == review_id).first()

        review.status = "Processing"
        db.commit()

        result = analyze_text(review.review_text)

        logger.info(f"AI Result: {result}")

        analytics = models.Analytics(
            review_id=review.id,
            sentiment=result["sentiment"],
            emotion=result["emotion"],
            confidence=result["confidence"]
        )

        db.add(analytics)

        review.status = "Completed"
        db.commit()

        logger.info(f"Review {review_id} processed successfully")

    except Exception as e:
        logger.error(f"Error processing review {review_id}: {str(e)}")

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
def get_reviews(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    reviews = db.query(models.Review).offset(skip).limit(limit).all()
    return reviews

@app.post("/submit-review")
def submit_review(data: schemas.ReviewCreate, bg: BackgroundTasks, db: Session = Depends(get_db)):
    
    try:
        logger.info(f"New review received for product {data.product_id}")

        review = crud.create_review(db, data.product_id, data.review_text)

        bg.add_task(process_review, review.id, db)

        return {"message": "Review submitted"}

    except Exception as e:
        logger.error(f"Error in submit-review: {str(e)}")
        return {"error": "Something went wrong"}

@app.get("/analytics-summary")
def analytics_summary(db: Session = Depends(get_db)):
    return crud.get_analytics_summary(db)

@app.get("/analytics")
def get_analytics(db: Session = Depends(get_db)):
    data = db.query(models.Analytics).all()
    return data

@app.put("/products/{product_id}")
def update_product(product_id: int, data: schemas.ProductCreate, db: Session = Depends(get_db)):
    result = crud.update_product(db, product_id, data.name, data.description)
    if result:
        return result
    return {"error": "Product not found"}


@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    result = crud.delete_product(db, product_id)
    if result:
        return {"message": "Product deleted"}
    return {"error": "Product not found"}