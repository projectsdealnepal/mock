from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class Gender(models.TextChoices):
    MALE = "M", "male"
    FEMALE = "F", "female"
    OTHER = "O", "other"


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    # date_of_birth = models.DateField(null=True, blank=True)
    # gender = models.CharField(max_length=1, null=True, blank=True, choices=Gender.choices)
    # contact_number = models.CharField(max_length=15, null=True, blank=True)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    EMAIL_FIELD = "email"
    updated_date = models.DateTimeField(_("updated date"), auto_now=True)
    # college

    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]
    USERNAME_FIELD = "username"

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name


class UserProfileExtraFields(models.Model):
    user = models.OneToOneField(
        CustomUser,
        verbose_name=_("user"),
        related_name="user_profile_extra_fields",
        on_delete=models.CASCADE,
    )
    gender = models.CharField(
        max_length=1, null=True, blank=True, choices=Gender.choices
    )
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    college_name = models.CharField(
        _("college name"), null=True, blank=True, max_length=150
    )
    college_location = models.CharField(
        _("college name"), null=True, blank=True, max_length=150
    )
    home_city = models.CharField(_("home city"), null=True, blank=True, max_length=150)
    current_city = models.CharField(
        _("current city"), null=True, blank=True, max_length=150
    )

    class Meta:
        verbose_name = _("UserProfileExtraField")
        verbose_name_plural = _("UserProfileExtraFields")

    def __str__(self):
        return str(self.pk)
