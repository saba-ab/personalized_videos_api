from django.contrib import admin
from .models import Payment
# Register your models here.


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'video_request', 'payment_id',
                    'payment_status', 'amount', 'currency', 'created_at', 'updated_at']
    list_filter = ['payment_status', 'currency', 'created_at', 'updated_at']
    search_fields = ['user__username', 'video_request__id', 'payment_id']
    readonly_fields = ['created_at', 'updated_at']
