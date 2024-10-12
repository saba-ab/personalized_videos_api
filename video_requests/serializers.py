from rest_framework import serializers
from .models import VideoRequest, Payment
from .enums import VideoType


class VideoRequestSerializer(serializers.ModelSerializer):
    video_type = serializers.ChoiceField(
        choices=VideoType.choices(), write_only=True)
    video_type_display = serializers.CharField(
        source="get_video_type_display", read_only=True)

    class Meta:
        model = VideoRequest
        fields = [
            'id',
            'user',
            'influencer',
            'video_for',
            'video_type',
            'video_type_display',
            'instructions',
            'birthdate',
            'turning',
            'public_permissions',
            'created_at',
            'updated_at',
            'amount'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'video_request', 'payment_id',
                  'amount', 'payment_status', 'created_at', 'updated_at']


class PaymentApprovalSerializer(serializers.Serializer):
    approval_url = serializers.URLField()
