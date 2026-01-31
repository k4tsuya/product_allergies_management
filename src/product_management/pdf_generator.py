"""Module for generating pdfs."""

from collections.abc import Sequence
from dataclasses import dataclass
from fpdf import FPDF
from src.product_management.allergens import ALLERGENS

# Set language for the output (Only English and Dutch supported.)
# Use "en" or "nl"
language: str = "nl"




@dataclass
class ProductAllergenView:
    name: str
    allergens: list[str]


def get_allergen_labels(language: str) -> dict[str, dict[str, str]]:
    return {
        code: {
        "label": data[language],
        "icon": data["icon"],
        }
        for code, data in ALLERGENS.items()
    }

def generate_allergen_matrix_pdf(
    data: Sequence[ProductAllergenView],
    output_path: str,
) -> None:
    """Generate a PDF of all products and their allergens."""

    allergen_labels = get_allergen_labels(language)
    allergen_codes = list(allergen_labels.keys())

    pdf = FPDF(orientation="L")
    pdf.add_page()
    pdf.set_font("Arial", size=8)

    # Title
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Allergen Matrix", ln=True)
    pdf.ln(3)

    # Column sizes
    product_col_width = 30
    allergen_col_width = 18
    row_height = 10

    # Header
    # Header: ICON ROW
    pdf.set_font("Arial", "B", 8)
    pdf.cell(product_col_width, row_height, "", border=1)

    for code in allergen_codes:
        x = pdf.get_x()
        y = pdf.get_y()

        pdf.cell(allergen_col_width, row_height, "", border=1)

        icon_size = 7

        icon_path = allergen_labels[code]["icon"]
        pdf.image(
            icon_path,
            x + (allergen_col_width - icon_size) / 2,
            y + (row_height - icon_size) / 2,
            w=icon_size,
            h=icon_size,
        )

    pdf.ln()

    # Header: LABEL ROW
    pdf.cell(product_col_width, row_height, "Product", border=1)

    for code in allergen_codes:
        label = allergen_labels[code]["label"]
        pdf.cell(allergen_col_width, row_height, label, border=1, align="C")

    pdf.ln()

    # Rows
    pdf.set_font("Arial", size=8)

    fill = False
    for product in data:
        if fill:
            pdf.set_fill_color(255, 255, 255)
        else:
            pdf.set_fill_color(235, 235, 235)
        fill = not fill

        pdf.cell(product_col_width, row_height, product.name, border=1, fill=True)

        for code in allergen_codes:
            mark = "x" if code in product.allergens else ""
            pdf.cell(
                allergen_col_width,
                row_height,
                mark,
                border=1,
                align="C",
                fill=True,
            )

        pdf.ln()

    pdf.output(output_path)