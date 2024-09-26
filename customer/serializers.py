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
         # Ensure either email or phone number is provided, but not both
        email = attrs.get('email')
        phone_number = attrs.get('phone_number')

        if not email and not phone_number:
            raise serializers.ValidationError("You must provide either an email or a phone number.")
        
        if email and phone_number:
            raise serializers.ValidationError("You can only provide one: either an email or a phone number, not both.")
        
        # Check if a user with the provided email or phone number already exists
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        
        if phone_number and User.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError("A user with this phone number already exists.")
        
        # Ensure passwords match
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
