from django.urls import path
from .views import user_inquiry_received_view

app_name = "blogs"

urlpatterns = [
    path('contact-us/',user_inquiry_received_view, name='user_inquiry_received_view')
]
