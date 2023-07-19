from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from dj_rest_auth.views import LoginView as DjLoginView

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    CustomTokenObtainPairSerializer,
    CustomLoginSerializer,
    UserProfileExtraFieldsSerializer,
)

from rest_framework.views import APIView
from .models import UserProfileExtraFields
from rest_framework.permissions import IsAuthenticated

from .serializers import ProfileDetailsSerializer

from rest_framework.exceptions import NotFound

from v1.question.models import ExamType
from v1.exam.models import UserExamType

# from django.http import


class EmailTokenObtainPairView(TokenObtainPairView):
    """
    Use to get the token pair using email and password
    """

    serializer_class = CustomTokenObtainPairSerializer


class LoginView(DjLoginView):
    def get_response(self):
        serializer = self.get_serializer(data=self.request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            user_data = CustomLoginSerializer(user).data
            return Response(
                {
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                    "user": user_data,
                }
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class KycStatusView(APIView):
    """
    This Api checks whether the user has filled up the profile or not.
    response: True, False
    If kyc or profile is not updated it response False otherwise True
    """
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            data = {"error": "User is not authenticated"}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

        user = self.request.user
        is_verified = hasattr(user, "user_profile_extra_fields")
        data = {"kyc_verified": is_verified}
        return Response(data, status=status.HTTP_200_OK)


kyc_status_view = KycStatusView.as_view()


class ProfileCreateUpdateView(APIView):
    """
    This api is for the user to update the profile.
    Allowed methods are:
    PUT and POST

    """

    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileExtraFieldsSerializer

    def verify_and_save_serializer(self, serializer):
        user = self.request.user
        first_name = serializer.validated_data.pop("first_name")
        last_name = serializer.validated_data.pop("last_name")
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        exam_types = serializer.validated_data.pop("exam_types", [])
        for exam_type_id in exam_types:
            try:
                exam_type = ExamType.objects.get(id=exam_type_id)
                UserExamType.objects.create(
                    user=self.request.user, exam_type=exam_type
                )
            except ExamType.DoesNotExist:
                pass
        serializer.save(user=user)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        profile_exists = UserProfileExtraFields.objects.filter(user=user).exists()
        if profile_exists:
            return Response(
                {"error": "User profile already exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            s_copy = serializer.validated_data.copy()
            self.verify_and_save_serializer(serializer)
            return Response(s_copy, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        try:
            profile = UserProfileExtraFields.objects.get(user=self.request.user)
        except UserProfileExtraFields.DoesNotExist:
            return Response(
                {"error": "User profile not found."}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.serializer_class(profile, data=request.data)
        if serializer.is_valid():
            s_copy = serializer.validated_data.copy()
            serializer.validated_data.pop("exam_types", [])
            self.verify_and_save_serializer(serializer)
            return Response(s_copy, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


profile_create_update_view = ProfileCreateUpdateView.as_view()


class ProfileDetailsView(APIView):
    """
    This api is for the user to get the profile details.
    Allowed methods are:
    GET

    """

    permission_classes = [IsAuthenticated]
    serializer_class = ProfileDetailsSerializer

    def get(self, *args, **kwargs):
        user = self.request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


profile_details_view = ProfileDetailsView.as_view()
