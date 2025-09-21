# models.py
from django.db import models
from django.utils import timezone

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, unique=True)
    monthly_income = models.DecimalField(max_digits=12, decimal_places=2)
    approved_limit = models.BigIntegerField()  # store rupees, integer
    current_debt = models.DecimalField(max_digits=15, decimal_places=2, default=0)

class Loan(models.Model):
    loan_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, related_name='loans', on_delete=models.CASCADE)
    loan_amount = models.DecimalField(max_digits=15, decimal_places=2)
    tenure_months = models.PositiveIntegerField()
    annual_interest_rate = models.DecimalField(max_digits=5, decimal_places=2)  # percent
    emi = models.DecimalField(max_digits=15, decimal_places=2)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    emIs_paid_on_time = models.PositiveIntegerField(default=0)  # count or more detailed table
    total_emis = models.PositiveIntegerField(default=0)
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
