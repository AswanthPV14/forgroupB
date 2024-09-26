"""import random
from django.core.mail import send_mail
from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password', 'is_customer', 'is_service_provider', 'phone_number']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        otp = random.randint(1000, 9999)
        email = validated_data['email']

        
        self.context['request'].session['otp'] = otp

        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        

        

       
        user = User.objects.create(
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            is_customer=validated_data.get('is_customer', False),
            is_service_provider=validated_data.get('is_service_provider', False),
            is_verified=False  
        )
        user.set_password(validated_data['password'])
        user.save()
        # In RegisterSerializer
        self.context['request'].session['otp'] = otp
        print(f"Stored OTP in session: {otp}")

        

        return user


class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')

        # Log the email and OTP being validated
        print(f"Email: {email}, OTP: {otp}")

        # Retrieve OTP from session (you can use cache or database as well)
        saved_otp = self.context['request'].session.get('otp')

        if not saved_otp:
            raise serializers.ValidationError("No OTP found for verification.")

        if otp != str(saved_otp):  # Ensure both are strings for comparison
            raise serializers.ValidationError("Invalid OTP.")

        # Fetch the user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist.")

        # Verify the user
        if user.is_verified:
            raise serializers.ValidationError("User is already verified.")

        user.is_verified = True
        user.save()

        return {"message": "User verified successfully."}"""






"""
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, OTP
from django.core.mail import send_mail
from .models import OTP
from phonenumber_field.serializerfields import PhoneNumberField  # Correct import

class UserRegistrationSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(required=False)  # Use this correctly
    email = serializers.EmailField(required=False)
    country_code = serializers.CharField(max_length=10, required=False)  # Optionally for display
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'country_code', 'password', 'confirm_password')

    def validate(self, attrs):
        # Check if either email or phone number is provided
        if not attrs.get('email') and not attrs.get('phone_number'):
            raise serializers.ValidationError("Either email or phone number is required.")

        # Check if passwords match
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError("Passwords do not match.")

        return attrs

    def create(self, validated_data):
        # Remove confirm_password from validated data
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)

        # Send OTP based on the registration method
        if validated_data.get('email'):
            self.send_otp_email(user, validated_data['email'])  # Pass the user instance
        elif validated_data.get('phone_number'):
            self.send_otp_sms(user, validated_data['phone_number'])  # Pass the user instance

        return user

    def send_otp_email(self, user, email):
        # Logic to send OTP to email
        otp = OTP.objects.create(user=user)  # Create OTP with the user instance
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp.otp_code}',
            'from@example.com',  # Replace with your sender email
            [email],
            fail_silently=False,
        )

    def send_otp_sms(self, user, phone_number):
        # Logic to print OTP for phone number in the terminal (for now)
        otp = OTP.objects.create(user=user)  # Create OTP with the user instance
        print(f"Sending OTP: {otp.otp_code} to phone number: {phone_number}")





class OTPVerifySerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=6)

    def validate(self, data):
        otp_code = data.get('otp_code')
        user = self.context['user']

        otp_instance = OTP.objects.filter(user=user).latest('created_at')

        if otp_instance and otp_instance.is_expired():
            raise serializers.ValidationError("OTP has expired.")
        
        if otp_instance and otp_instance.otp_code != otp_code:
            raise serializers.ValidationError("Invalid OTP code.")

        return data
"""

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, OTP
from django.core.mail import send_mail
from phonenumber_field.serializerfields import PhoneNumberField  

class UserRegistrationSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField(required=False)  
    email = serializers.EmailField(required=False)
    country_code = serializers.CharField(max_length=10, required=False)  
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'country_code', 'password', 'confirm_password')

    def validate(self, attrs):
        
        if not attrs.get('email') and not attrs.get('phone_number'):
            raise serializers.ValidationError("Either email or phone number is required.")

       
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError("Passwords do not match.")

        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create_user(**validated_data)

        
        if validated_data.get('email'):
            self.send_otp_email(user, validated_data['email'])  
        elif validated_data.get('phone_number'):
            self.send_otp_sms(user, validated_data['phone_number'])  

        return user

    def send_otp_email(self, user, email):
        # Logic to send OTP to email
        otp = OTP.objects.create(user=user)  # Create OTP with the user instance
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp.otp_code}',
            None,  # Uses DEFAULT_FROM_EMAIL from settings
            [email],  # Use email from the registration
            fail_silently=False,
        )

    def send_otp_sms(self, user, phone_number):
        # Logic to print OTP for phone number in the terminal (for now)
        otp = OTP.objects.create(user=user)  # Create OTP with the user instance
        print(f"Sending OTP: {otp.otp_code} to phone number: {phone_number}")

class OTPVerifySerializer(serializers.Serializer):
    otp_code = serializers.CharField(max_length=6)

    def validate(self, data):
        otp_code = data.get('otp_code')
        user = self.context['user']

        otp_instance = OTP.objects.filter(user=user).latest('created_at')

        if otp_instance and otp_instance.is_expired():
            raise serializers.ValidationError("OTP has expired.")
        
        if otp_instance and otp_instance.otp_code != otp_code:
            raise serializers.ValidationError("Invalid OTP code.")

        return data
