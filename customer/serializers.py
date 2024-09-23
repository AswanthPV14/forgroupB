from rest_framework import serializers
from .models import Customer
from django.contrib.auth.hashers import make_password

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Customer
        fields = ['email', 'password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}} 

    def validate(self, data):
        
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        validated_data['password'] = make_password(validated_data['password'])
        user = Customer.objects.create(**validated_data)
        return user
    
class OtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
