from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.billing_service import generate_bill

router = APIRouter(prefix="/billing", tags=["Billing"])


@router.post("/")
def create_bill(request: dict, db: Session = Depends(get_db)):
    return generate_bill(
        db=db,
        email=request["email"],
        items=request["items"],
        cash_paid=request["cash_paid"]
    )
