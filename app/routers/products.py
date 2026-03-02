from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product
from app.crud import create_product, get_all_products

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/")
def read_products(db: Session = Depends(get_db)):
    return get_all_products(db)


@router.post("/")
def add_product(product_data: dict, db: Session = Depends(get_db)):
    return create_product(db, product_data)
