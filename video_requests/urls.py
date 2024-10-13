from django.urls import path, include
from .views import VideoRequestCreateView, VideoRequestListView, CreatePaymentView, ExecutePaymentView

urlpatterns = [
    path('create/', VideoRequestCreateView.as_view(),
         name='video_request_create'),
    path('list/', VideoRequestListView.as_view(), name='video_request_list'),
    path('<int:pk>/', VideoRequestListView.as_view(),
         name='video_request_detail'),
    path('create-payment/<int:video_request_id>/',
         CreatePaymentView.as_view(), name='create_payment'),
    path('execute-payment/', ExecutePaymentView.as_view(), name='execute_payment'),
]
