from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product
from app.services.billing_service import generate_bill
from fastapi.templating import Jinja2Templates
from fastapi import BackgroundTasks
from app.services.email_service import send_invoice_email

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def billing_page(request: Request, db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return templates.TemplateResponse("billing_page.html", {
        "request": request,
        "products": products
    })


@router.post("/generate-bill", response_class=HTMLResponse)
def generate_bill_web(
    request: Request,
    background_tasks: BackgroundTasks,
    email: str = Form(...),
    product_ids: list[str] = Form(...),
    quantities: list[int] = Form(...),
    cash_paid: float = Form(...),
    db: Session = Depends(get_db)
):

    items = []

    for i in range(len(product_ids)):
        if int(quantities[i]) > 0:
            items.append({
                "product_id": product_ids[i],
                "quantity": int(quantities[i])
            })

    try:
        result = generate_bill(db, email, items, cash_paid)

        # 🔥 Async Email Trigger
        background_tasks.add_task(
            send_invoice_email,
            email,
            result
        )

        return templates.TemplateResponse("bill_result.html", {
            "request": request,
            "result": result
        })

    except Exception as e:
        return templates.TemplateResponse("billing_page.html", {
            "request": request,
            "error": str(e),
            "products": db.query(Product).all()
        })
