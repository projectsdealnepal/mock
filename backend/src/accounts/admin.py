from django.contrib import admin
from .models import CustomUser, UserProfileExtraFields

# Register your models here.


class CustomUserModelAdmin(admin.ModelAdmin):
    list_display = [
        "email",
        "first_name",
        "last_name",
        "is_staff",
    ]


admin.site.register(CustomUser, CustomUserModelAdmin)


class UserProfileExtraFieldsModelAdmin(admin.ModelAdmin):
    list_display = [
        "user_email",
        "gender",
        "contact_number",
        "date_of_birth",
        "college_name",
        "college_location",
        "home_city",
        "current_city",
    ]

    def user_email(Self, obj):
        return obj.user.email

    user_email.short_description = "email"


admin.site.register(UserProfileExtraFields, UserProfileExtraFieldsModelAdmin)
