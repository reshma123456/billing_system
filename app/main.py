
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.database import engine, Base, SessionLocal
import app.models  # registers all models
from app.routers import products, billing, history, web

from app.crud import create_product
from app.models import Product
from fastapi.responses import FileResponse

# -------------------------------
# Create FastAPI App
# -------------------------------
app = FastAPI(title="Billing System")

# -------------------------------
#  Create Database Tables
# -------------------------------
Base.metadata.create_all(bind=engine)

# -------------------------------
#  Templates & Static Files
# -------------------------------
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("app/static/favicon.ico")

# -------------------------------
#  Seed Products on Startup
# -------------------------------
@app.on_event("startup")
def seed_products():
    db = SessionLocal()

    try:
        if db.query(Product).count() == 0:
            products = [
                {
                    "product_id": "P101",
                    "name": "Laptop",
                    "available_stock": 10,
                    "price": 50000,
                    "tax_percentage": 18
                },
                {
                    "product_id": "P102",
                    "name": "Mouse",
                    "available_stock": 50,
                    "price": 500,
                    "tax_percentage": 5
                },
                {
                    "product_id": "P103",
                    "name": "Keyboard",
                    "available_stock": 30,
                    "price": 1000,
                    "tax_percentage": 12
                }
            ]

            for product in products:
                create_product(db, product)

    finally:
        db.close()


# -------------------------------
#  Include Routers
# -------------------------------

app.include_router(products.router)
app.include_router(billing.router)
app.include_router(history.router)
app.include_router(web.router)

