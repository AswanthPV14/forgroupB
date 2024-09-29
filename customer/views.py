from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import ServiceRequest, Booking
from .serializers import ServiceRequestSerializer, BookingSerializer
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Service App Home Page")


class ServiceRequestViewSet(viewsets.ModelViewSet):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer
    permission_classes = [IsAuthenticated]

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

class ServiceRequestCreateView(generics.CreateAPIView):
    queryset = ServiceRequest.objects.all()
    serializer_class = ServiceRequestSerializer

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

class BookingListView(generics.ListAPIView):
    queryset = Booking.objects.filter(request__acceptance_status='accept')
    serializer_class = BookingSerializer

class BookingDetailView(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer




