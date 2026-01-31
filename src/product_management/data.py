"""Module for inserting data into the database."""

from sqlalchemy.orm import Session

from src.product_management.models import Allergen, Product
from src.product_management.allergens import ALLERGENS



# NVWA allergen list (simplified)


SAMPLE_PRODUCTS = {
    "Frikandel": ["gluten", "soy", "mustard"],
    "Kroket": ["gluten", "milk"],
    "Bread": ["gluten"],
    "Fishstick": ["fish"],
}

def load_allergens(db: Session) -> None:
    """Insert allergens into the db if they don't exist."""
    for code, data in ALLERGENS.items():
        en = data["en"]
        nl = data["nl"]
        if db.query(Allergen).filter_by(code=code).first():
            continue

        db.add(
            Allergen(
                code=code,
                description_en=en,
                description_nl=nl,
            )
        )

    db.commit()


def load_products(db: Session) -> None:
    """Insert products into the db with the corresponding allergens."""

    data_source: dict = SAMPLE_PRODUCTS

    allergens_by_code = {
        allergen.code: allergen
        for allergen in db.query(Allergen).all()
    }

    # To use real data, create product_list.py in the same directory of this module
    # and create a JSON structure like the SAMPLE_PRODUCTS.
    try:
        from src.product_management.product_list import products
        data_source = products
    except ImportError:
        print("Real data not found. Loading sample data...")



    for name, allergen_codes in data_source.items():
        if db.query(Product).filter_by(name=name).first():
            continue

        product = Product(name=name)

        for code in allergen_codes:
            product.allergens.append(allergens_by_code[code])

        db.add(product)

    db.commit()