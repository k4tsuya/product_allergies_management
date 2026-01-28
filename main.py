"""Main module for the product management app."""

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from src.product_management.data import load_allergens, load_products
from src.product_management.models import Base, SessionLocal, engine
from src.product_management.schemas import ProductResponse
from src.product_management.queries import list_allergens, list_products, get_gluten_free_products

app = FastAPI(title="Snack Bar Product API")


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        load_allergens(db)
        load_products(db)


@app.get("/products", response_model=list[ProductResponse])
def list_all_products(db: Session = Depends(get_db)):
    """Return all products."""
    return list_products(db)

@app.get("/gluten-free", response_model=list[ProductResponse])
def list_gluten_free_products(db: Session = Depends(get_db)):
    """Return all gluten-free products."""
    return get_gluten_free_products(db)


@app.get("/allergens")
def list_all_allergens(db: Session = Depends(get_db)):
    """Return all allergens."""
    return list_allergens(db)