# Snack Bar Product & Allergen Management

## 📌 Project Overview

This project started from a **real, practical need** at my current **part-time job** in a snackbar in the Netherlands.

As a food business, we are legally required to:

* Maintain a clear and correct **allergen list**
* Be able to tell customers **which allergens are present in which products**
* Follow EU / NVWA (Nederlandse Voedsel- en Warenautoriteit) food allergen regulations

Managing this information manually quickly became error‑prone and time‑consuming. This project is my attempt to **solve that real-world problem with software**, while at the same time **learning and exploring new backend and frontend technologies**.

---

## 🚧 Project Status

This project is **actively under development** and is being built step by step as a learning project.

It is intended to become part of my **developer portfolio**, showcasing how I approach real-world backend problems, data modeling, frontend development, and new technologies.

---

## 🎯 Goals of This Project

* Model food allergens **correctly and realistically**
* Link allergens to products in a flexible way
* Create a clean and understandable backend foundation
* Build a working, presentable frontend to consume that backend
* Learn and practice technologies I have not used deeply before
* Build a meaningful portfolio project based on real business needs

---

## 🧠 Domain Modeling

A key design decision in this project is **how allergens are modeled**.

* Allergens are **not boolean fields** on a product
* Allergens are a **fixed, regulated list** (EU / NVWA)
* Products can contain **multiple allergens**
* One allergen can apply to **multiple products**

Because of this, the project uses a **many‑to‑many relationship** between:

* `Product`
* `Allergen`

This approach:

* Matches real‑world legislation
* Avoids fragile database schemas
* Makes the system easy to extend in the future (e.g. "may contain traces of")

---

## 🧱 Tech Stack

I intentionally chose this tech stack to **learn and explore different tools** beyond what I already knew.

**Backend**
* **Python 3.13**
* **FastAPI** – modern, fast backend framework
* **SQLAlchemy 2.0** – ORM with explicit, type‑safe models
* **SQLite** – simple local database for development
* **Pydantic** – data validation and API schemas

**Frontend**
* **React** – component-based UI library
* **Vite** – frontend build tool and dev server

Although I have previous experience with **Django + DRF**, this project focuses on:

* Understanding lower‑level ORM concepts
* Explicit database modeling
* Clear separation between models, schemas, and application logic
* Learning frontend development from the ground up with React

---

## 🗂️ Project Structure (backend)

```
src/product_management/
├── core/
│   └── database.py       # DB engine/session setup
├── models.py               # SQLAlchemy models
├── schemas.py               # Pydantic schemas
├── queries.py                # DB query functions
├── seed/
│   ├── insert_data.py         # Functions that insert data into the DB
│   ├── products.py             # Real product data (gitignored, see below)
│   └── allergens.py            # NVWA allergen reference data
├── pdf_generator.py           # PDF export logic
└── static/
    └── icons/                # Allergen icons, served via FastAPI static files
```

---

## 🧪 Example Data

The application automatically seeds:

### Allergens (simplified example)

* Gluten
* Milk
* Soy
* Mustard

### Products

* **Frikandel** → gluten, soy, mustard
* **Kroket** → gluten, milk
* **Bread** → gluten
* **Fishstick** → fish

This data is inserted on application startup and is safe to run multiple times.

---

## 🚀 Running the Project

The backend and frontend run as two separate servers during development.

### 1. Backend setup

```bash
pip install fastapi uvicorn sqlalchemy pydantic fpdf
```

Set the preferred language for the generated PDF file via the `language` variable in the `download_products_pdf()` function (`main.py`), set to `'en'` or `'nl'`.

Start the backend:

```bash
uvicorn main:app --reload
```

The API is now available at `http://localhost:8000`, with interactive docs at:

```
http://localhost:8000/docs
```

### 2. Frontend setup

In a separate terminal:

```bash
cd frontend
npm install
npm run dev -- --host
```

The frontend is now available at `http://localhost:5173`.

Both servers must be running at the same time for the frontend to fetch data from the backend. CORS is configured on the backend to allow requests from `http://localhost:5173`.

---

## 🔍 Available Endpoints

* `GET /products` – list products with their allergens
* `GET /allergens` – list all known allergens
* `GET /products/pdf` – generate a downloadable PDF file
* `GET /static/icons/{filename}` – serves allergen icon images

---

## 📚 What I Learned From This Project

* How to model **many‑to‑many relationships** correctly
* The difference between **ORM models** and **API schemas**
* How to translate **legal/business requirements** into data models
* React fundamentals: components, props, state, effects, conditional rendering
* Connecting a React frontend to a FastAPI backend (CORS, fetch, serving static files)
* Structuring a growing codebase into clear, single-purpose modules

---

## 🤖 Learning React with AI

I'm learning React as part of this project, and I've been using **Claude** as a learning tool throughout that process — asking it to explain concepts step by step (state, props, `.map()`, conditional rendering, etc.), review and refactor code, and help debug issues as they come up.

I see this as similar to using a tutorial, documentation, or a mentor: the AI helps me understand *why* something works the way it does, but the implementation decisions, debugging, and understanding are still mine to build. I'm noting this openly here since transparency about how I learn and build matters to me, especially in a portfolio project.

---

## 🔮 Future Improvements

Planned extensions include:

* Product creation via API (`POST /products`)
* Support for **"may contain traces of"** allergens
* Search / filter functionality on the frontend
* Runtime language switching (Dutch/English toggle) instead of a fixed setting

---

## 📦 Product Data Source

This project ships with sample product data for demo and development purposes.

By default, the application loads data from an internal sample dataset: `SAMPLE_PRODUCTS`, defined in `src/product_management/seed/insert_data.py`.

### Using real product data

If you want to use your own (real) product data, you can provide it via a file that is intentionally excluded from version control.

Create a file at:

```
src/product_management/seed/products.py
```

Define a variable called `products` with the same structure as `SAMPLE_PRODUCTS`:

```python
products = {
    "Example product": ["gluten", "milk"],
    "Another product": ["nuts"],
}
```

When present, the application will automatically load this data instead of the sample data. If the file is not found, the system safely falls back to the sample dataset.

This approach allows:

* Running the project out-of-the-box
* Keeping real business data private
* Avoiding configuration or environment variables for simple setups

**Note:** `src/product_management/seed/products.py` is listed in `.gitignore` to keep real business data out of version control.

---

## 💬 Final Note

This project is part of my **personal learning journey and portfolio** and will continue to evolve over time.

This project is intentionally **practical**.

It represents how I approach development:

* Start from real requirements
* Model the domain carefully
* Prefer clarity over complexity
* Learn by building — including learning openly with the help of AI tools

Feedback and suggestions are always welcome.