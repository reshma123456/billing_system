#  Billing Management System

A full-stack Billing Management System built using **FastAPI**, **PostgreSQL**, and **Docker**.

This application allows users to:

- Generate customer bills
- Automatically calculate tax
- Manage product stock
- Compute balance denominations
- Send invoice emails
- Persist data in PostgreSQL
- Run the entire system using Docker containers

---

##  Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Templating**: Jinja2
- **Containerization**: Docker & Docker Compose
- **Email Service**: SMTP (Gmail App Password)

---

##  Project Architecture
app/
│
├── main.py # FastAPI app initialization
├── database.py # DB engine & session setup
├── models.py # SQLAlchemy models
├── crud.py # DB operations
│
├── routers/
│ └── web.py # Web routes
│
├── services/
│ ├── billing_service.py # Core billing logic
│ └── email_service.py # Invoice email logic
│
├── templates/
│ ├── billing_page.html
│ └── bill_result.html
│
docker-compose.yml
Dockerfile
requirements.txt
README.md

##  Features

###  Billing
- Multiple products per bill
- Dynamic tax calculation
- Net total calculation
- Rounded total calculation

###  Inventory
- Automatic stock deduction
- Insufficient stock validation

###  Denomination Calculation
- Automatic balance denomination breakdown
- Supports: 500, 50, 20, 10, 5, 2, 1

###  Email Integration
- Sends invoice email after bill generation
- Uses Gmail App Password

###  Dockerized
- FastAPI container
- PostgreSQL container
- Persistent database volume

---

##  Running with Docker 

### 1️. Clone Repository

git clone https://github.com/reshma123456/billing_system.git
cd billing_system

### 2. Create .env File

Create a .env file in the root directory:

SENDER_EMAIL=yourgmail@gmail.com
SENDER_PASSWORD=your_gmail_app_password
DATABASE_URL=postgresql://postgres:postgres@db:5432/billing_db

### 3️. Build and Run Containers
docker compose up --build

Or run in detached mode:

docker compose up -d --build

### 4️. Access Application

Open:

http://localhost:8000

### 5️. Stop Containers
docker compose down

To reset database completely:

docker compose down -v

## Running Without Docker (Development Mode)

### 1️.Create Virtual Environment
python -m venv venv

Activate:

Windows:

venv\Scripts\activate

### 2️. Install Dependencies
pip install -r requirements.txt

### 3️.Setup PostgreSQL

Create database:

CREATE DATABASE billing_db;

Update .env:

DATABASE_URL=postgresql://postgres:password@localhost:5432/billing_db

### 4️.Run Application
uvicorn app.main:app --reload

Open:

http://127.0.0.1:8000

#### Database Tables

products

customers

bills

bill_items

denominations