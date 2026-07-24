from src.product_management.models import Product, Allergen


def test_list_products_endpoint_returns_empty_list_when_no_products(client):
    response = client.get("/products")

    assert response.status_code == 200
    assert response.json() == []


def test_list_products_endpoint_returns_seeded_product(client, db_session):
    db_session.add(Product(name="Frikandel"))
    db_session.commit()

    response = client.get("/products")

    assert response.status_code == 200
    assert response.json()[0]["name"] == "Frikandel"


def test_list_allergens_endpoint(client, db_session):
    db_session.add(Allergen(code="gluten", description_en="Gluten", description_nl="Gluten"))
    db_session.commit()

    response = client.get("/allergens")

    assert response.status_code == 200
    assert response.json()[0]["code"] == "gluten"


def test_gluten_free_endpoint_excludes_gluten_products(client, db_session):
    gluten = Allergen(code="gluten", description_en="Gluten", description_nl="Gluten")
    product_with_gluten = Product(name="Bread", allergens=[gluten])
    product_without_gluten = Product(name="Fishstick")

    db_session.add_all([product_with_gluten, product_without_gluten])
    db_session.commit()

    response = client.get("/gluten-free")

    names = [p["name"] for p in response.json()]
    assert names == ["Fishstick"]


def test_download_pdf_endpoint_returns_pdf_file(client, db_session):
    gluten = Allergen(code="gluten", description_en="Gluten", description_nl="Gluten")
    product = Product(name="Bread", allergens=[gluten])
    db_session.add(product)
    db_session.commit()

    response = client.get("/products/pdf")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"