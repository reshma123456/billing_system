from sqlalchemy.orm import Session
from app.models import Product, Bill, BillItem
from app.crud import get_customer_by_email, create_customer


from sqlalchemy.orm import Session
from app.models import Product, Bill, BillItem, Denomination
from app.crud import get_customer_by_email, create_customer


def calculate_denominations(balance_amount: int):

    denominations_available = [500, 200, 100, 50, 20, 10, 5, 2, 1]

    result = []
    remaining = balance_amount

    for denom in denominations_available:
        if remaining >= denom:
            count = remaining // denom
            remaining = remaining % denom

            result.append({
                "denomination_value": denom,
                "count": count
            })

    return result


def generate_bill(db: Session, email: str, items: list, cash_paid: float):

    try:
        # 1️⃣ Get or Create Customer
        customer = get_customer_by_email(db, email)
        if not customer:
            customer = create_customer(db, email)

        total_without_tax = 0
        total_tax = 0

        # 2️⃣ Create Bill (initially empty totals)
        bill = Bill(
            customer_id=customer.id,
            total_without_tax=0,
            total_tax=0,
            net_total=0,
            rounded_total=0,
            cash_paid=cash_paid,
            balance_amount=0
        )

        db.add(bill)
        db.flush()  # 🔥 Needed to get bill.id before commit

        # 3️⃣ Process Each Item
        for item in items:

            product = db.query(Product).filter(
                Product.product_id == item["product_id"]
            ).first()

            if not product:
                raise Exception(f"Product {item['product_id']} not found")

            if product.available_stock < item["quantity"]:
                raise Exception(f"Insufficient stock for {product.name}")

            purchase_price = product.price * item["quantity"]
            tax_amount = (purchase_price * product.tax_percentage) / 100
            total_price = purchase_price + tax_amount

            total_without_tax += purchase_price
            total_tax += tax_amount

            # 🔥 Reduce Stock
            product.available_stock -= item["quantity"]

            bill_item = BillItem(
                bill_id=bill.id,
                product_id=product.id,
                quantity=item["quantity"],
                unit_price=product.price,
                tax_percentage=product.tax_percentage,
                tax_amount=tax_amount,
                total_price=total_price
            )

            db.add(bill_item)

        # 4️⃣ Final Calculations
        net_total = total_without_tax + total_tax
        rounded_total = int(net_total)
        balance_amount = cash_paid - rounded_total

        if balance_amount < 0:
            raise Exception("Insufficient cash paid")

        # Update bill totals
        bill.total_without_tax = total_without_tax
        bill.total_tax = total_tax
        bill.net_total = net_total
        bill.rounded_total = rounded_total
        bill.balance_amount = balance_amount

        # 5️⃣ Calculate Denominations
        denomination_data = calculate_denominations(int(balance_amount))

        for denom in denomination_data:
            db.add(Denomination(
                bill_id=bill.id,
                denomination_value=denom["denomination_value"],
                count=denom["count"]
            ))

        # 6️⃣ Commit Transaction
        db.commit()

        return {
            "message": "Bill generated successfully",
            "bill_id": bill.id,
            "total_without_tax": total_without_tax,
            "total_tax": total_tax,
            "net_total": net_total,
            "rounded_total": rounded_total,
            "cash_paid": cash_paid,
            "balance_amount": balance_amount,
            "denominations": denomination_data
        }

    except Exception as e:
        db.rollback()
        raise e


def calculate_denominations(balance_amount: int):

    denominations_available = [500, 200, 100, 50, 20, 10, 5, 2, 1]

    result = []

    remaining = balance_amount

    for denom in denominations_available:
        if remaining >= denom:
            count = remaining // denom
            remaining = remaining % denom

            result.append({
                "denomination_value": denom,
                "count": count
            })

    return result
