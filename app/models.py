from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class BillItem(Base):
    __tablename__ = "bill_items"

    id = Column(Integer, primary_key=True, index=True)

    bill_id = Column(Integer, ForeignKey("bills.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    quantity = Column(Integer)
    unit_price = Column(Float)
    tax_percentage = Column(Float)
    tax_amount = Column(Float)
    total_price = Column(Float)

    bill = relationship("Bill", back_populates="items")
    product = relationship("Product", back_populates="bill_items")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, unique=True, index=True)
    name = Column(String, nullable=False)
    available_stock = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    tax_percentage = Column(Float, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    bill_items = relationship("BillItem", back_populates="product")

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    bills = relationship("Bill", back_populates="customer")


class Bill(Base):
    __tablename__ = "bills"

    id = Column(Integer, primary_key=True, index=True)

    customer_id = Column(Integer, ForeignKey("customers.id"))

    total_without_tax = Column(Float)
    total_tax = Column(Float)
    net_total = Column(Float)
    rounded_total = Column(Float)
    cash_paid = Column(Float)
    balance_amount = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="bills")
    items = relationship("BillItem", back_populates="bill")
    denominations = relationship("Denomination", back_populates="bill")


class Denomination(Base):
    __tablename__ = "denominations"

    id = Column(Integer, primary_key=True, index=True)

    bill_id = Column(Integer, ForeignKey("bills.id"))

    denomination_value = Column(Integer)
    count = Column(Integer)

    bill = relationship("Bill", back_populates="denominations")
