from src.product_management.models import Product, Allergen
from src.product_management.queries import (
    list_products,
    list_allergens,
    get_gluten_free_products,
    pdf_list_products,
)


def test_list_products_returns_all_products(db_session):
    db_session.add(Product(name="Frikandel"))
    db_session.add(Product(name="Kroket"))
    db_session.commit()

    result = list_products(db_session)

    assert len(result) == 2


def test_list_allergens_returns_sorted_by_description(db_session):
    db_session.add(Allergen(code="soy", description_en="Soy", description_nl="Soja"))
    db_session.add(Allergen(code="gluten", description_en="Gluten", description_nl="Gluten"))
    db_session.commit()

    result = list_allergens(db_session)

    assert [a.description_en for a in result] == ["Gluten", "Soy"]


def test_get_gluten_free_products_excludes_gluten(db_session):
    gluten = Allergen(code="gluten", description_en="Gluten", description_nl="Gluten")
    milk = Allergen(code="milk", description_en="Milk", description_nl="Melk")

    kroket = Product(name="Kroket", allergens=[gluten, milk])
    fishstick = Product(name="Fishstick", allergens=[milk])

    db_session.add_all([kroket, fishstick])
    db_session.commit()

    result = get_gluten_free_products(db_session)

    assert [p.name for p in result] == ["Fishstick"]


def test_pdf_list_products_returns_correct_shape(db_session):
    gluten = Allergen(code="gluten", description_en="Gluten", description_nl="Gluten")
    product = Product(name="Bread", allergens=[gluten])

    db_session.add(product)
    db_session.commit()

    result = pdf_list_products(db_session)

    assert len(result) == 1
    assert result[0].name == "Bread"
    assert result[0].allergens == ["gluten"]