from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from .models import VideoRequest, Payment
from .serializers import VideoRequestSerializer, PaymentApprovalSerializer
import paypalrestsdk
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter

paypalrestsdk.configure({
    'mode': 'sandbox',  # Change to 'live' for production
    'client_id': settings.PAYPAL_CLIENT_ID,
    'client_secret': settings.PAYPAL_CLIENT_SECRET
})


class VideoRequestCreateView(generics.CreateAPIView):
    queryset = VideoRequest.objects.all()
    serializer_class = VideoRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.is_anonymous:
            raise NotAuthenticated(
                detail='You must be logged in to create a video request')
        serializer.save(user=self.request.user)


class VideoRequestListView(generics.ListAPIView):
    serializer_class = VideoRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return VideoRequest.objects.filter(user=self.request.user)


class CreatePaymentView(APIView):
    serializer_class = PaymentApprovalSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Create PayPal Payment",
        description="Initiate a PayPal payment for a video request.",
        responses={
            302: OpenApiResponse(description='Redirect to PayPal approval URL'),
            400: OpenApiResponse(description='Payment creation error')
        }
    )
    def post(self, request, video_request_id):
        video_request = get_object_or_404(VideoRequest, id=video_request_id)
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": "http://127.0.0.1:8000/api/payment/execute",
                "cancel_url": "http://127.0.0.1:8000/api/payment/cancel"
            },
            "transactions": [{
                "item_list": {
                    "items": [{
                        "name": f"Video request for {video_request.video_for}",
                        "sku": "video_request",
                        "price": str(video_request.amount),
                        "currency": "USD",
                        "quantity": 1
                    }]
                },
                "amount": {
                    "total": str(video_request.amount),
                    "currency": "USD"
                },
                "description": f"Payment for video request {video_request.id}"
            }]
        })

        if payment.create():
            Payment.objects.create(
                user=request.user,
                video_request=video_request,
                payment_id=payment.id,
                amount=video_request.amount
            )
            for link in payment.links:
                if link.rel == "approval_url":
                    # return redirect(link.href)
                    return Response({'approval_url': link.href}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': payment.error}, status=status.HTTP_400_BAD_REQUEST)


class ExecutePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Execute PayPal Payment",
        description="Complete the PayPal payment after user approval.",
        parameters=[
            OpenApiParameter(name='paymentId', location=OpenApiParameter.QUERY,
                             description='PayPal payment ID', required=True, type=str),
            OpenApiParameter(name='PayerID', location=OpenApiParameter.QUERY,
                             description='PayPal payer ID', required=True, type=str)
        ],
        responses={
            200: OpenApiResponse(description='Payment executed successfully'),
            400: OpenApiResponse(description='Payment execution error')
        }
    )
    def get(self, request):
        payment_id = request.GET.get('paymentId')
        payer_id = request.GET.get('PayerID')
        payment = paypalrestsdk.Payment.find(payment_id)

        if payment.execute({"payer_id": payer_id}):
            Payment.objects.filter(payment_id=payment_id).update(
                payment_status='Completed')
            return JsonResponse({'message': 'Payment executed successfully!'}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': payment.error}, status=status.HTTP_400_BAD_REQUEST)
