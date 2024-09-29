from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import uuid

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class ServiceRequest(models.Model):
    SERVICE_CATEGORIES = [
        ('Home Maintenance', 'Home Maintenance'),
        ('Home Appliance Repair', 'Home Appliance Repair'),
        ('Laundry Service', 'Laundry Service'),
        ('Business Services', 'Business Services'),
        ('Cleaning Services', 'Cleaning Services'),
        ('Electronics Repair', 'Electronics Repair'),
        ('Delivery Services', 'Delivery Services'),
        ('Technology Services', 'Technology Services'),
        ('Health and Fitness', 'Health and Fitness'),
        ('Essential Services', 'Essential Services'),
        ('Vehicles & Transport', 'Vehicles & Transport'),
        ('Home Renovation', 'Home Renovation'),
        ('Beauty Services', 'Beauty Services'),
    ]

    SUB_CATEGORIES = [
        ('Urgent', 'Urgently needed'),
        ('Plan for later', 'Plan for later'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    service = models.CharField(max_length=255)
    category = models.CharField(choices=SERVICE_CATEGORIES, max_length=50)
    sub_category = models.CharField(choices=SUB_CATEGORIES, max_length=50, default='Plan for later')
    description = models.TextField()
    image = models.ImageField(upload_to='service_images/', blank=True, null=True)
    availability_from = models.DateTimeField()
    availability_to = models.DateTimeField()
    address = models.CharField(max_length=255)
    additional_notes = models.TextField(blank=True, null=True)
    work_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    acceptance_status = models.CharField(max_length=20, choices=[('accept', 'accept'), ('decline', 'decline'), ('pending', 'pending')], default='pending')
    request_date = models.DateTimeField(auto_now_add=True)
    service_charge = models.DecimalField(max_digits=6, decimal_places=2)
    customer = models.ForeignKey(User, related_name='requests', on_delete=models.CASCADE)
    service_provider = models.ForeignKey(User, related_name='providers', on_delete=models.CASCADE)

    def clean(self):
        if self.availability_from >= self.availability_to:
            raise ValidationError('Availability "from" time must be before "to" time.')

class Booking(models.Model):
    request = models.OneToOneField(ServiceRequest, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    payment_status = models.BooleanField(default=False)

    def accept_payment(self):
        self.payment_status = True
        self.save()


   
