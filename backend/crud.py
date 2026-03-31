from sqlalchemy.orm import Session
from sqlalchemy import func
import models

def create_product(db: Session, name: str, description: str):
    product = models.Product(name=name, description=description)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def create_review(db: Session, product_id: int, review_text: str):
    review = models.Review(product_id=product_id, review_text=review_text)
    db.add(review)
    db.commit()
    db.refresh(review)
    return review

def get_products(db: Session):
    return db.query(models.Product).all()

def get_reviews(db: Session):
    return db.query(models.Review).all()

def get_analytics_summary(db):
    total_reviews = db.query(models.Analytics).count()

    positive = db.query(models.Analytics).filter(models.Analytics.sentiment == "POSITIVE").count()

    negative = db.query(models.Analytics).filter(models.Analytics.sentiment == "NEGATIVE").count()

    avg_confidence = db.query(func.avg(models.Analytics.confidence)).scalar()

    return {
        "total_reviews": total_reviews,
        "positive": positive,
        "negative": negative,
        "avg_confidence": avg_confidence
    }

def update_product(db, product_id, name, description):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        product.name = name
        product.description = description
        db.commit()
        return product
    return None


def delete_product(db, product_id):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
        return True
    return False