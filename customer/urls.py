from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceRequestViewSet, BookingViewSet, ServiceRequestCreateView, BookingListView, BookingDetailView

router = DefaultRouter()
router.register(r'service-requests', ServiceRequestViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('service/request/', ServiceRequestCreateView.as_view(), name='service-request'),
    path('bookings/', BookingListView.as_view(), name='bookings-list'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
]

