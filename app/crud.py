from sqlalchemy.orm import Session
from app import models

from app.models import Customer
from app.models import Bill



def create_product(db: Session, product_data: dict):
    product = models.Product(**product_data)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_all_products(db: Session):
    return db.query(models.Product).all()



def get_customer_by_email(db: Session, email: str):
    return db.query(Customer).filter(Customer.email == email).first()


def create_customer(db: Session, email: str):
    customer = Customer(email=email)
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer


def get_bills_by_customer_email(db: Session, email: str):
    return (
        db.query(Bill)
        .join(Bill.customer)
        .filter(Bill.customer.has(email=email))
        .all()
    )

def get_bill_by_id(db: Session, bill_id: int):
    return db.query(Bill).filter(Bill.id == bill_id).first()

