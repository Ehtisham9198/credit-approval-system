from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Customer
from .serializers import CustomerSerializer
import math

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
