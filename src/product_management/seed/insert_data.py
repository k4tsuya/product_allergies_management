"""Module for inserting data into the database."""

from sqlalchemy.orm import Session

from src.product_management.core.config import ENABLE_MEAT_TRACKING
from src.product_management.models import Allergen, MeatType, Product
from src.product_management.seed.allergens import ALLERGENS
from src.product_management.seed.meat_types import MEAT_TYPES

SAMPLE_PRODUCTS = {
    "Frikandel": ["gluten", "soy", "mustard"],
    "Kroket": ["gluten", "milk"],
    "Bread": ["gluten"],
    "Fishstick": ["fish"],
}

SAMPLE_PRODUCT_MEAT_TYPES = {
    "Frikandel": ["pork", "beef"],
    "Kroket": ["beef"],
    "Bread": [],
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


def load_meat_types(db: Session) -> None:
    """Insert meat types into the db if they don't exist."""
    for code, data in MEAT_TYPES.items():
        en = data["en"]
        nl = data["nl"]
        if db.query(MeatType).filter_by(code=code).first():
            continue

        db.add(
            MeatType(
                code=code,
                description_en=en,
                description_nl=nl,
            )
        )

    db.commit()


def load_products(db: Session) -> None:
    """Insert products into the db with the corresponding allergens."""

    data_source: dict = SAMPLE_PRODUCTS
    meat_data_source: dict = SAMPLE_PRODUCT_MEAT_TYPES

    allergens_by_code = {
        allergen.code: allergen
        for allergen in db.query(Allergen).all()
    }

    meat_types_by_code = {}
    if ENABLE_MEAT_TRACKING:
        meat_types_by_code = {
            meat_type.code: meat_type
            for meat_type in db.query(MeatType).all()
        }

    # To use real data, create products.py in the same directory of this module
    # and create a JSON structure like the SAMPLE_PRODUCTS.
    try:
        from src.product_management.seed.products import products
        data_source = products
    except ImportError:
        print("Real data not found. Loading sample data...")

    # To use real meat type data, create product_meat_types.py in the same
    # directory as this module, with the same structure as SAMPLE_PRODUCT_MEAT_TYPES.
    try:
        from product_management.seed.meat_types import product_meat
        meat_data_source = product_meat
    except ImportError:
        pass

    for name, allergen_codes in data_source.items():
        if db.query(Product).filter_by(name=name).first():
            continue

        product = Product(name=name)

        for code in allergen_codes:
            product.allergens.append(allergens_by_code[code])

        if ENABLE_MEAT_TRACKING:
            meat_codes = meat_data_source.get(name, [])
            for code in meat_codes:
                product.meat_types.append(meat_types_by_code[code])

        db.add(product)

    db.commit()