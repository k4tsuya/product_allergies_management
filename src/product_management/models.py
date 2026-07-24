"""Module containing models for the product management app."""

from sqlalchemy import Column, ForeignKey, Numeric, String, Table
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

from src.product_management.core.database import engine, SessionLocal

class Base(DeclarativeBase):
    pass


product_allergen = Table(
    "product_allergen",
    Base.metadata,
    Column("product_id", ForeignKey("products.id"), primary_key=True),
    Column("allergen_id", ForeignKey("allergens.id"), primary_key=True),
)

product_meat_type = Table(
    "product_meat_type",
    Base.metadata,
    Column("product_id", ForeignKey("products.id"), primary_key=True),
    Column("meat_type_id", ForeignKey("meat_types.id"), primary_key=True),
)


class Allergen(Base):
    __tablename__ = "allergens"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description_en: Mapped[str] = mapped_column(String(200), nullable=False)
    description_nl: Mapped[str] = mapped_column(String(200), nullable=False)

    products: Mapped[list["Product"]] = relationship(
        secondary=product_allergen,
        back_populates="allergens",
    )


class MeatType(Base):
    __tablename__ = "meat_types"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    description_en: Mapped[str] = mapped_column(String(200), nullable=False)
    description_nl: Mapped[str] = mapped_column(String(200), nullable=False)

    products: Mapped[list["Product"]] = relationship(
        secondary=product_meat_type,
        back_populates="meat_types",
    )


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    units_per_box: Mapped[int] = mapped_column(nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=True)

    allergens: Mapped[list[Allergen]] = relationship(
        secondary=product_allergen,
        back_populates="products",
    )
    meat_types: Mapped[list["MeatType"]] = relationship(
        secondary=product_meat_type,
        back_populates="products",
    )