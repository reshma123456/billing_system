# from fastapi import FastAPI
# from sqlalchemy.orm import Session
# from fastapi import Depends

# from app.database import engine, Base, get_db, SessionLocal
# import app.models  # VERY IMPORTANT - registers models

# from app.models import Product
# from app.crud import create_product
# from app.routers import products
# from app.routers import billing
# from app.routers import history


# # 🔥 1️⃣ Create FastAPI App
# app = FastAPI(title="Billing System API")


# # 🔥 2️⃣ Create Tables
# Base.metadata.create_all(bind=engine)


# # 🔥 3️⃣ Seed Products on Startup
# @app.on_event("startup")
# def seed_products():
#     db = SessionLocal()

#     if db.query(Product).count() == 0:
#         products_data = [
#             {
#                 "product_id": "P101",
#                 "name": "Laptop",
#                 "available_stock": 10,
#                 "price": 50000,
#                 "tax_percentage": 18
#             },
#             {
#                 "product_id": "P102",
#                 "name": "Mouse",
#                 "available_stock": 50,
#                 "price": 500,
#                 "tax_percentage": 5
#             },
#             {
#                 "product_id": "P103",
#                 "name": "Keyboard",
#                 "available_stock": 30,
#                 "price": 1000,
#                 "tax_percentage": 12
#             }
#         ]

#         for product in products_data:
#             create_product(db, product)

#     db.close()


# # 🔥 4️⃣ Include Routers
# app.include_router(products.router)
# app.include_router(billing.router)
# app.include_router(history.router)


# # 🔥 5️⃣ Root Endpoint
# @app.get("/")
# def read_root():
#     return {"message": "Billing System Running Successfully"}


# @app.get("/products")
# def read_products(db: Session = Depends(get_db)):
#     return db.query(Product).all()



from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.database import engine, Base, SessionLocal
import app.models  # VERY IMPORTANT - registers all models

from app.crud import create_product
from app.models import Product
from fastapi.responses import FileResponse

# -------------------------------
# 1️⃣ Create FastAPI App
# -------------------------------
app = FastAPI(title="Billing System")

# -------------------------------
# 2️⃣ Create Database Tables
# -------------------------------
Base.metadata.create_all(bind=engine)

# -------------------------------
# 3️⃣ Templates & Static Files
# -------------------------------
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/favicon.ico")
async def favicon():
    return FileResponse("app/static/favicon.ico")

# -------------------------------
# 4️⃣ Seed Products on Startup
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

# # -------------------------------
# # 5️⃣ Root Health Check
# # -------------------------------
# @app.get("/")
# def root():
#     return {"message": "Billing System Running Successfully"}

# -------------------------------
# 6️⃣ Include Routers
# -------------------------------
from app.routers import products, billing, history, web

app.include_router(products.router)
app.include_router(billing.router)
app.include_router(history.router)
app.include_router(web.router)

