from django.shortcuts import render

# Create your views here.
import razorpay
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.conf import settings
from customer.models import Invoice, Payment
from .serializers import InvoiceSerializer, PaymentSerializer
import razorpay
import json
from django.urls import reverse
import hmac
import hashlib





class CreatePaymentOrderAPIView(APIView):
    def post(self, request):
        try:
            invoice_id = request.data.get('invoice_id')
            if not invoice_id:
                return Response({"error": "invoice_id is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            invoice = Invoice.objects.get(id=invoice_id)
            serializer = InvoiceSerializer(invoice)

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            payment_amount = int(invoice.total_amount * 100)

            payment_data = {
                'amount': payment_amount,
                'currency': 'INR',
                'receipt': f"inv_{invoice.id}",
                'payment_capture': 1,  # Auto capture the payment
            }

            order = client.order.create(data=payment_data)

            # Create payment with 'pending' status
            payment = Payment.objects.create(
                invoice=invoice,
                sender=invoice.sender,
                receiver=invoice.receiver,
                transaction_id=order['id'],  # Initial transaction ID (same as order ID for now)
                order_id=order['id'],  # Razorpay order_id
                amount_paid=invoice.total_amount,
                payment_method='razorpay',
                payment_status='pending',  # Set status to 'pending'
            )

            payment_serializer = PaymentSerializer(payment)

            return Response({
                'order_id': order['id'],
                'amount': order['amount'],
                'currency': order['currency'],
                'invoice': serializer.data,
                'payment': payment_serializer.data,
            }, status=status.HTTP_201_CREATED)

        except Invoice.DoesNotExist:
            return Response({'error': 'Invoice not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



def payment_view(request):
    return render(request, 'payment/payment.html', {
        'razorpay_key': settings.RAZORPAY_KEY_ID  # Pass the Razorpay key to the template
    })
   



class VerifyPaymentAPIView(APIView):
    def post(self, request):
        try:
            razorpay_payment_id = request.data.get('razorpay_payment_id')
            razorpay_order_id = request.data.get('razorpay_order_id')
            razorpay_signature = request.data.get('razorpay_signature')

            if not all([razorpay_payment_id, razorpay_order_id, razorpay_signature]):
                return Response({"error": "Required fields are missing"}, status=status.HTTP_400_BAD_REQUEST)

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            # Fetch payment details from Razorpay
            payment_details = client.payment.fetch(razorpay_payment_id)

            # Signature verification
            generated_signature = hmac.new(
                bytes(settings.RAZORPAY_KEY_SECRET, 'utf-8'),
                msg=bytes(f"{razorpay_order_id}|{razorpay_payment_id}", 'utf-8'),
                digestmod=hashlib.sha256
            ).hexdigest()

            if generated_signature != razorpay_signature:
                return Response({"error": "Invalid signature"}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch the payment record using the order ID
            try:
                payment_record = Payment.objects.get(order_id=razorpay_order_id)
            except Payment.DoesNotExist:
                return Response({'error': 'Payment with this order ID not found'}, status=status.HTTP_404_NOT_FOUND)

            # Update payment record with Razorpay details
            payment_record.transaction_id = razorpay_payment_id
            payment_record.signature = razorpay_signature

            # Process payment status
            
            payment_status = payment_details['status']
            if payment_status == 'captured':
                payment_record.mark_completed()  # Set status to 'completed'
            elif payment_status == 'failed':
                payment_record.mark_failed()
            else:
                payment_record.payment_status = 'pending'
                

            payment_record.save()

            return Response({
                'transaction_id': payment_record.transaction_id,
                'order_id': razorpay_order_id,
                'amount': payment_record.amount_paid,
                'status': payment_record.payment_status,
                'payment_details': payment_details
            }, status=status.HTTP_200_OK)

        except razorpay.errors.BadRequestError as e:
            return Response({'error': 'Bad Request: {}'.format(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

            

