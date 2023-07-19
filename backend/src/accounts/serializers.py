from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from .models import UserProfileExtraFields, Gender
from v1.question.models import ExamType

# not needed for now
# from v1.exam.models import UserExamType
# from v1.question.serializers import ExamTypeSerializer as ExamTypeSerializerForProfile

User = get_user_model()


class CustomLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pk", "username", "email", "first_name", "last_name")


class CustomRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("pk", "email")


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer for obtaining the JWT token pair using an email address and password.
    """

    username_field = User.EMAIL_FIELD


class ExamTypeSerializer(serializers.ModelSerializer):
    exam_type_id = serializers.SerializerMethodField()

    class Meta:
        model = ExamType
        fields = ("exam_type_id",)

    def get_exam_type_id(self, obj):
        return obj.pk


class UserProfileExtraFieldsSerializer(serializers.ModelSerializer):
    gender = serializers.ChoiceField(choices=Gender.choices)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    # exam_types = ExamTypeSerializer(many=True)
    exam_types = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = UserProfileExtraFields
        fields = (
            "first_name",
            "last_name",
            "gender",
            "contact_number",
            "date_of_birth",
            "college_name",
            "college_location",
            "home_city",
            "current_city",
            "exam_types",
        )

    # def validate_exam_types(self, data):
    #     print(data)
    #     if not isinstance(data, list):
    #         serializers.ValidationError('exam_types must be list')

    #     return data


# not implemented
# class UserExamTypeSerializerForProfile(serializers.ModelSerializer):
#     exam_type = ExamTypeSerializerForProfile()

#     class Meta:
#         model = UserExamType
#         fields = ("exam_type",)


class ProfileDetailsSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    date_joined = serializers.DateTimeField()
    gender = serializers.ChoiceField(
        choices=Gender.choices, source="user_profile_extra_fields.gender"
    )
    contact_number = serializers.CharField(
        source="user_profile_extra_fields.contact_number"
    )
    date_of_birth = serializers.DateField(
        source="user_profile_extra_fields.date_of_birth"
    )
    college_name = serializers.CharField(
        source="user_profile_extra_fields.college_name"
    )
    college_location = serializers.CharField(
        source="user_profile_extra_fields.college_location"
    )
    home_city = serializers.CharField(source="user_profile_extra_fields.home_city")
    current_city = serializers.CharField(
        source="user_profile_extra_fields.current_city"
    )

    # exam_type = UserExamTypeSerializerForProfile(source="user_exam_types", many=True)
    exam_types = serializers.SerializerMethodField()

    def get_exam_types(self, obj):
        # gets the user_exam_types related to that particular user
        exam_types_queryset = obj.user_exam_types.prefetch_related("exam_type")
        # using manual list to get the required format
        exam_types_list = [
            {
                "id": exam_type.exam_type.id,
                "name": exam_type.exam_type.name,
                "short_form": exam_type.exam_type.short_form,
            }
            for exam_type in exam_types_queryset.all()
        ]
        return exam_types_list
