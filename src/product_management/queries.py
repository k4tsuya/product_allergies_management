"""Queries for the product management app."""
from src.product_management.models import Product, Allergen
from sqlalchemy.orm import Session


def list_products(db: Session):
    """Query all products."""
    return db.query(Product).all()

def list_allergens(db: Session):
    """Query all allergens."""
    return db.query(Allergen).order_by(Allergen.description_en).all()

def get_gluten_free_products(db: Session) -> list[Product]:
    """Query all gluten-free products."""
    return (db.query(Product).filter(~Product.allergens.any(Allergen.code == "gluten")).all())