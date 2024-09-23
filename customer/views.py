
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Customer
from .serializers import RegistrationSerializer, OtpSerializer
from django.shortcuts import render
import random

@api_view(['POST'])
def register(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        # Generate OTP
        otp = str(random.randint(100000, 999999))
        user = Customer.objects.get(email=request.data['email'])
        user.otp = otp
        user.save()

        # In a real app, you would send this OTP via email or SMS
        print(f"OTP for {user.email}: {otp}")

        return Response({'message': 'User registered. OTP sent to email.'}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def verify_otp(request):
    serializer = OtpSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = Customer.objects.get(email=serializer.validated_data['email'])
            if user.otp == serializer.validated_data['otp']:
                return Response({'message': 'OTP verified successfully.'})
            return Response({'error': 'Invalid OTP'}, status=400)
        except Customer.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
    return Response(serializer.errors, status=400)

def home(request):
    return render(request, 'customer/register.html')


