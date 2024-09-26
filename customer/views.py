"""from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer, OTPVerifySerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered. Check your email for OTP."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch')
class OTPVerifyView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = OTPVerifySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)"""






"""from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, OTP
from .serializers import UserRegistrationSerializer, OTPVerifySerializer

class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Save user and retrieve the user object
            return Response({'message': 'User registered successfully. OTP sent to the provided contact method.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    def post(self, request, *args, **kwargs):
        # Determine if the contact method is email or phone number
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')

        # Fetch the user based on the contact method
        user = None
        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        elif phone_number:
            try:
                user = User.objects.get(phone_number=phone_number)
            except User.DoesNotExist:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Contact method not provided.'}, status=status.HTTP_400_BAD_REQUEST)

        # Proceed with OTP verification
        serializer = OTPVerifySerializer(data=request.data, context={'user': user})
        if serializer.is_valid():
            # Optionally delete OTP after successful verification
            otp_instance = OTP.objects.filter(user=user).latest('created_at')
            otp_instance.delete()  # Delete or mark as used
            return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)"""






from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, OTP
from .serializers import UserRegistrationSerializer, OTPVerifySerializer

class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Save user and retrieve the user object
            return Response({'message': 'User registered successfully. OTP sent to the provided contact method.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        phone_number = request.data.get('phone_number')

        # Fetch the user based on the contact method
        user = None
        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        elif phone_number:
            try:
                user = User.objects.get(phone_number=phone_number)
            except User.DoesNotExist:
                return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Contact method not provided.'}, status=status.HTTP_400_BAD_REQUEST)

        # Proceed with OTP verification
        serializer = OTPVerifySerializer(data=request.data, context={'user': user})
        if serializer.is_valid():
            # Optionally delete OTP after successful verification
            otp_instance = OTP.objects.filter(user=user).latest('created_at')
            otp_instance.delete()  # Delete or mark as used
            return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

