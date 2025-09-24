Got it 👍 — here’s the **full README.md** formatted properly for your project:

```markdown
# 💳 Credit Approval System (Django + DRF + Celery + Postgres + Redis)

This project is a **backend-only Credit Approval System** built using **Django Rest Framework (DRF)**.  
It evaluates customer loan eligibility, processes loan creation, and maintains loan records.  
Data ingestion is handled in the background using **Celery workers with Redis**.

---

## 🚀 Features
- Customer registration with auto-calculated credit limit.
- Loan eligibility check based on:
  - Past repayment history
  - Active loans & approved limits
  - Loan activity in the current year
- Loan creation with EMI calculation (compound interest).
- View single loan details.
- View all loans by a customer.
- Background ingestion of Excel data (`customer_data.xlsx` & `loan_data.xlsx`) using Celery.
- **Dockerized** setup with `docker-compose` (single command run).

---

## 🛠 Tech Stack
- **Backend**: Python 3.11, Django 5, Django REST Framework  
- **Database**: PostgreSQL  
- **Task Queue**: Celery + Redis  
- **Containerization**: Docker & Docker Compose  

---

## 📂 Project Structure
```

credit-approval-system/
│── core/                 # Main app (models, views, serializers, tasks)
│── credit\_system/        # Django project (settings, celery app, urls, wsgi)
│── requirements.txt      # Dependencies
│── Dockerfile            # Docker build instructions
│── docker-compose.yml    # Multi-container setup
│── entrypoint.sh         # Entrypoint for Docker web service
└── README.md             # Project documentation

````

---

## ⚡ Setup & Run

### 🔹 1. Clone Repository
```bash
git clone https://github.com/<your-username>/credit-approval-system.git
cd credit-approval-system
````

### 🔹 2. Environment Setup (local run without Docker)

```bash
python -m venv creditenv
source creditenv/bin/activate
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver
```

### 🔹 3. Run with Docker Compose

Make sure Docker is installed and running. Then:

```bash
docker compose up -d --build
```

This starts:

* **Postgres** at `localhost:5432`
* **Redis** at `localhost:6379`
* **Django API** at `http://127.0.0.1:8000`

---

## 📊 API Endpoints

### 1️⃣ Register Customer

**POST** `/register`

Request Body:

```json
{
  "first_name": "Ehtisham",
  "last_name": "Ali",
  "age": 25,
  "monthly_income": 40000,
  "phone_number": "9876543210"
}
```

Response:

```json
{
  "customer_id": 1,
  "name": "Ehtisham Ali",
  "age": 25,
  "monthly_income": 40000,
  "approved_limit": 1440000,
  "phone_number": "9876543210"
}
```

---

### 2️⃣ Check Loan Eligibility

**POST** `/check-eligibility`

Request Body:

```json
{
  "customer_id": 1,
  "loan_amount": 50000,
  "interest_rate": 10,
  "tenure": 12
}
```

Response:

```json
{
  "customer_id": 1,
  "approval": true,
  "interest_rate": 10,
  "corrected_interest_rate": 12,
  "tenure": 12,
  "monthly_installment": 4500.0,
  "message": "Loan approved"
}
```

---

### 3️⃣ Create Loan

**POST** `/create-loan`

Request Body:

```json
{
  "customer_id": 1,
  "loan_amount": 50000,
  "interest_rate": 10,
  "tenure": 12
}
```

Response:

```json
{
  "loan_id": 1,
  "customer_id": 1,
  "loan_approved": true,
  "message": "Loan created successfully",
  "monthly_installment": 4500.0
}
```

---

### 4️⃣ View Loan

**GET** `/view-loan/<loan_id>`

Response:

```json
{
  "loan_id": 1,
  "customer": {
    "id": 1,
    "first_name": "Ehtisham",
    "last_name": "Ali",
    "phone_number": "9876543210",
    "age": 25
  },
  "loan_amount": 50000,
  "interest_rate": 12.0,
  "monthly_installment": 4500.0,
  "tenure": 12,
  "approved": true
}
```

---

### 5️⃣ View All Loans of a Customer

**GET** `/view-loans/<customer_id>`

Response:

```json
[
  {
    "loan_id": 1,
    "loan_amount": 50000,
    "interest_rate": 12.0,
    "monthly_installment": 4500.0,
    "repayments_left": 10
  },
  {
    "loan_id": 2,
    "loan_amount": 30000,
    "interest_rate": 10.0,
    "monthly_installment": 2800.0,
    "repayments_left": 8
  }
]
```

---

## 🗄 Background Data Import (Celery)

Run Celery worker:

```bash
celery -A credit_system worker -l info
```

Trigger data import:

```python
from core.tasks import import_customers, import_loans

import_customers.delay("/home/user/customer_data.xlsx")
import_loans.delay("/home/user/loan_data.xlsx")
```

---

## 🐳 Docker Notes

* To rebuild and restart:

```bash
docker compose down
docker compose up -d --build
```

* Logs:

```bash
docker compose logs -f
```

---

## ✅ Assignment Completion Checklist

* [x] Register API
* [x] Check Eligibility API
* [x] Create Loan API
* [x] View Loan API
* [x] View All Loans API
* [x] Background data ingestion with Celery
* [x] PostgreSQL + Redis setup
* [x] Dockerized with `docker-compose`

---

## 👨‍💻 Author

**Mohd Ehtisham**
📧 \[Your Email]
🔗 [GitHub Profile](https://github.com/Ehtisham9198)

```

---

Do you also want me to add **sample `docker-compose.yml` and Dockerfile** sections inside the README for reference (so the evaluator doesn’t need to open them separately)?
```
