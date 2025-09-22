from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Customer
from .serializers import CustomerSerializer
import math
from django.utils import timezone
from datetime import date
from decimal import Decimal
from dateutil.relativedelta import relativedelta


def evaluate_loan_eligibility(customer, loan_amount, interest_rate, tenure):
    """
    Core business logic for loan eligibility.
    Returns dict with approval, corrected_rate, emi, message.
    """
    # 1. Placeholder credit score (TODO: improve later)
    credit_score = 50  

    # 2. Apply credit score slab
    corrected_rate = interest_rate
    approval = True
    message = "Loan approved"

    if credit_score > 50:
        pass
    elif 30 < credit_score <= 50:
        if interest_rate < 12:
            corrected_rate = 12
    elif 10 < credit_score <= 30:
        if interest_rate < 16:
            corrected_rate = 16
    else:
        return {
            "approval": False,
            "corrected_rate": interest_rate,
            "emi": 0,
            "message": "Loan not approved due to low credit score"
        }

    # 3. Calculate EMI
    emi = calculate_emi(loan_amount, corrected_rate, tenure)

    # 4. Reject if EMI > 50% of salary
    if emi > 0.5 * float(customer.monthly_income):
        return {
            "approval": False,
            "corrected_rate": corrected_rate,
            "emi": emi,
            "message": "Loan not approved because EMI exceeds 50% of income"
        }

    return {
        "approval": True,
        "corrected_rate": corrected_rate,
        "emi": emi,
        "message": message
    }

@api_view(['POST'])
def register_customer(request):
    data = request.data
    approved_limit = round((36 * data['monthly_income']) / 100000) * 100000

    customer = Customer.objects.create(
        first_name=data['first_name'],
        last_name=data['last_name'],
        age=data['age'],
        monthly_income=data['monthly_income'],
        phone_number=data['phone_number'],
        approved_limit=approved_limit,
        current_debt=0
    )
    serializer = CustomerSerializer(customer)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def calculate_emi(principal, annual_rate, tenure_months):
    """
    Calculate EMI using compound interest formula
    """
    monthly_rate = (annual_rate / 100) / 12
    if monthly_rate == 0:  # edge case: 0% interest
        return round(principal / tenure_months, 2)

    emi = (principal * monthly_rate * (1 + monthly_rate) ** tenure_months) / \
          ((1 + monthly_rate) ** tenure_months - 1)
    return round(emi, 2)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Customer, Loan
import math
from datetime import date


def calculate_emi(principal, annual_rate, tenure_months):
    """
    Calculate EMI using compound interest formula
    """
    monthly_rate = (annual_rate / 100) / 12
    if monthly_rate == 0:  # edge case: 0% interest
        return round(principal / tenure_months, 2)

    emi = (principal * monthly_rate * (1 + monthly_rate) ** tenure_months) / \
          ((1 + monthly_rate) ** tenure_months - 1)
    return round(emi, 2)


@api_view(['POST'])
def check_eligibility(request):
    data = request.data
    customer_id = data.get("customer_id")
    loan_amount = float(data.get("loan_amount"))
    interest_rate = float(data.get("interest_rate"))
    tenure = int(data.get("tenure"))

    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=404)

    result = evaluate_loan_eligibility(customer, loan_amount, interest_rate, tenure)

    return Response({
        "customer_id": customer_id,
        "approval": result["approval"],
        "interest_rate": interest_rate,
        "corrected_interest_rate": result["corrected_rate"],
        "tenure": tenure,
        "monthly_installment": result["emi"],
        "message": result["message"]
    })


@api_view(['POST'])
def create_loan(request):
    data = request.data
    customer_id = data.get("customer_id")
    loan_amount = float(data.get("loan_amount"))
    interest_rate = float(data.get("interest_rate"))
    tenure = int(data.get("tenure"))

    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=404)

    # Use the helper function directly
    result = evaluate_loan_eligibility(customer, loan_amount, interest_rate, tenure)

    if not result["approval"]:
        return Response({
            "loan_id": None,
            "customer_id": customer_id,
            "loan_approved": False,
            "message": result["message"],
            "monthly_installment": result["emi"],
        }, status=200)

    # Create loan
    start = timezone.now().date()
    end = start + relativedelta(months=+tenure)

    loan = Loan.objects.create(
        customer=customer,
        loan_amount=Decimal(loan_amount),
        tenure_months=tenure,
        annual_interest_rate=Decimal(result["corrected_rate"]),
        emi=Decimal(result["emi"]),
        start_date=start,
        end_date=end,
        approved=True,
        total_emis=tenure,
        emIs_paid_on_time=0
    )

    # Update customer debt
    customer.current_debt = (customer.current_debt or 0) + loan.loan_amount
    customer.save()

    return Response({
        "loan_id": loan.loan_id,
        "customer_id": customer.customer_id,
        "loan_approved": True,
        "message": "Loan created successfully",
        "monthly_installment": float(loan.emi)
    }, status=201)


    
    
@api_view(['GET'])
def view_loan(request, loan_id):
    try:
        loan = Loan.objects.select_related('customer').get(loan_id=loan_id)
    except Loan.DoesNotExist:
        return Response({"error":"Loan not found"}, status=404)

    customer = loan.customer
    return Response({
        "loan_id": loan.loan_id,
        "customer": {
            "id": customer.customer_id,
            "first_name": customer.first_name,
            "last_name": customer.last_name,
            "phone_number": customer.phone_number,
            "age": customer.age
        },
        "loan_amount": float(loan.loan_amount),
        "interest_rate": float(loan.annual_interest_rate),
        "monthly_installment": float(loan.emi),
        "tenure": loan.tenure_months,
        "approved": loan.approved
    })
    
    
    
@api_view(['GET'])
def view_loans(request, customer_id):
    try:
        customer = Customer.objects.get(customer_id=customer_id)
    except Customer.DoesNotExist:
        return Response({"error": "Customer not found"}, status=404)

    loans = Loan.objects.filter(customer=customer, approved=True)

    response = []
    for loan in loans:
        # repayments left = total_emis - paid_emis
        repayments_left = loan.total_emis - loan.emIs_paid_on_time
        response.append({
            "loan_id": loan.loan_id,
            "loan_amount": float(loan.loan_amount),
            "interest_rate": float(loan.annual_interest_rate),
            "monthly_installment": float(loan.emi),
            "repayments_left": repayments_left
        })

    return Response(response, status=200)
