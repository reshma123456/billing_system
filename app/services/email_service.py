import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()


def send_invoice_email(to_email: str, bill_details: dict):

    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")

    subject = f"Invoice - Bill ID {bill_details['bill_id']}"

    body = f"""
    Invoice Details:

    Bill ID: {bill_details['bill_id']}
    Total Without Tax: {bill_details['total_without_tax']}
    Total Tax: {bill_details['total_tax']}
    Net Total: {bill_details['net_total']}
    Rounded Total: {bill_details['rounded_total']}
    Cash Paid: {bill_details['cash_paid']}
    Balance Amount: {bill_details['balance_amount']}

    Thank you for shopping with us.
    """

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())

    except smtplib.SMTPAuthenticationError as e:
        print(" AUTHENTICATION ERROR")
        print("Error Code:", e.smtp_code)
        print("Error Message:", e.smtp_error)

    except smtplib.SMTPConnectError as e:
        print(" CONNECTION ERROR")
        print(e)

    except smtplib.SMTPException as e:
        print(" SMTP ERROR")
        print(e)

    except Exception as e:
        print(" GENERAL ERROR")
        print(e)
