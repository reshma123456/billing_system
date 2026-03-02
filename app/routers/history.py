from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import get_bills_by_customer_email, get_bill_by_id

router = APIRouter(prefix="/history", tags=["History"])


@router.get("/{email}")
def get_customer_bills(email: str, db: Session = Depends(get_db)):
    return get_bills_by_customer_email(db, email)


@router.get("/bill/{bill_id}")
def get_bill_details(bill_id: int, db: Session = Depends(get_db)):
    bill = get_bill_by_id(db, bill_id)

    if not bill:
        return {"message": "Bill not found"}

    return {
        "bill_id": bill.id,
        "customer_email": bill.customer.email,
        "total_without_tax": bill.total_without_tax,
        "total_tax": bill.total_tax,
        "net_total": bill.net_total,
        "rounded_total": bill.rounded_total,
        "cash_paid": bill.cash_paid,
        "balance_amount": bill.balance_amount,
        "items": [
            {
                "product_name": item.product.name,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "tax_percentage": item.tax_percentage,
                "tax_amount": item.tax_amount,
                "total_price": item.total_price
            }
            for item in bill.items
        ],
        "denominations": [
            {
                "denomination_value": d.denomination_value,
                "count": d.count
            }
            for d in bill.denominations
        ]
    }
