from celery import shared_task
import pandas as pd
from .models import Customer, Loan
from decimal import Decimal

@shared_task
def import_customers(file_path="customer_data.xlsx"):
    df = pd.read_excel(file_path)
    for _, row in df.iterrows():
        Customer.objects.update_or_create(
            customer_id=row["customer_id"],
            defaults={
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "phone_number": row["phone_number"],
                "monthly_income": row["monthly_salary"],
                "approved_limit": row["approved_limit"],
                "current_debt": row["current_debt"],
            }
        )

@shared_task
def import_loans(file_path="loan_data.xlsx"):
    df = pd.read_excel(file_path)
    for _, row in df.iterrows():
        Loan.objects.update_or_create(
            loan_id=row["loan id"],
            defaults={
                "customer_id": row["customer id"],
                "loan_amount": Decimal(row["loan amount"]),
                "tenure_months": row["tenure"],
                "annual_interest_rate": Decimal(row["interest rate"]),
                "emi": Decimal(row["monthly repayment (emi)"]),
                "emIs_paid_on_time": row["EMIs paid on time"],
                "start_date": row["start date"],
                "end_date": row["end date"],
                "approved": True,
                "total_emis": row["tenure"],
            }
        )
