from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserInquirySerializer
from rest_framework.response import Response
from rest_framework import status
from tools import send_email

# Create your views here.
class UserInquiryReceiveView(APIView):
    """
    This views handles the user enquiry and send email to the user.
    """
    serializer_class = UserInquirySerializer
    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data = self.request.data)
        if serializer.is_valid():
            serializer.save()
            response_data = {
                'detail': 'message received successfully'
            }
            # send email will be implemented here.
            # send_email()
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
user_inquiry_received_view = UserInquiryReceiveView.as_view()