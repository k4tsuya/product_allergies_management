"""Main module for the product management app."""

from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session
from pathlib import Path
from src.product_management.seed.insert_data import load_allergens, load_meat_types, load_products
from src.product_management.core.database import SessionLocal, engine
from src.product_management.models import Base
from src.product_management.schemas import ProductResponse
from src.product_management.queries import list_allergens, list_products, get_gluten_free_products, pdf_list_products
from src.product_management.pdf_generator import AllergenMatrixPDF
from src.product_management.core.config import ENABLE_MEAT_TRACKING


from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        load_allergens(db)
        if ENABLE_MEAT_TRACKING:
            load_meat_types(db)
        load_products(db)

    yield


app = FastAPI(title="Snack Bar Product API", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="src/product_management/static"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """Report whether the API and database are reachable."""
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "unreachable"

    return {"status": "ok", "database": db_status}

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



BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "generated"
OUTPUT_DIR.mkdir(exist_ok=True)


@app.get("/products/pdf", response_class=FileResponse)
def download_products_pdf(language: str = "nl", db: Session = Depends(get_db)):
    """Save a PDF of all products and their allergens."""

    products = pdf_list_products(db)
    file_path = OUTPUT_DIR / "product_allergens.pdf"

    pdf = AllergenMatrixPDF(orientation="L")
    pdf.set_language(language)
    pdf.generate_allergen_matrix_pdf(
        data=products,
        output_path=str(file_path),
        language=language
    )

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename="products_allergens.pdf",
    )