from .models import UserInquiry
from rest_framework import serializers


class UserInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model=UserInquiry
        fields=(
            "first_name",
            "last_name",
            "email",
            "message",
        )

