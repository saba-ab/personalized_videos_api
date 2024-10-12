from django.db import models
from django.conf import settings
from .enums import VideoType
from enumfields import EnumField


class VideoRequest(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='video_requests')
    influencer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='influencer_requests',
        limit_choices_to={'is_influencer': True}
    )
    video_for = models.CharField(max_length=255)
    video_type = EnumField(VideoType, max_length=69, default=VideoType.OTHER)
    instructions = models.TextField()
    birthdate = models.DateField(blank=True, null=True)
    turning = models.IntegerField(blank=True, null=True)
    public_permissions = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self) -> str:
        return f'Video request from {self.user.username} to {self.influencer.username}'


class Payment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments',
    )
    video_request = models.OneToOneField(
        VideoRequest,
        on_delete=models.CASCADE,
        related_name='payment',
    )
    payment_id = models.CharField(max_length=255, unique=True)
    payment_status = models.CharField(max_length=50, default='Pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'Payment for video request {self.video_request} by {self.user.username}'
