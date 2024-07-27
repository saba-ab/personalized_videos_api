# videos/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from .models import Influencer, VideoRequest, Payment
from .serializers import InfluencerSerializer, VideoRequestSerializer, PaymentSerializer, UserSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample


class InfluencerViewSet(viewsets.ModelViewSet):
    queryset = Influencer.objects.all()
    serializer_class = InfluencerSerializer

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Influencer created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VideoRequestViewSet(viewsets.ModelViewSet):
    queryset = VideoRequest.objects.all()
    serializer_class = VideoRequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def make_payment(self, request, pk=None):
        video_request = self.get_object()
        # Integrate with a payment gateway
        payment_data = {
            'request': video_request.id,
            'amount': 10.00,  # Replace with actual amount
            'status': 'pending',
            'transaction_id': 'txn_12345'  # Replace with actual transaction ID
        }
        serializer = PaymentSerializer(data=payment_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


class UserViewSet(viewsets.ViewSet):
    @extend_schema(
        request=UserSerializer,
        responses={201: UserSerializer},
        description="Register a new user",
    )
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
