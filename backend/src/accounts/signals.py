from django.dispatch import receiver
from django.db.models.signals import post_save

# from dj_rest_auth.registration import user_registered
from v1.package.models import Package
from django.contrib.auth.models import User


# @receiver(post_save, sender=User)
# def assign_default_package(sender, instance, created, **kwargs):
#     """
#     This signal function assigns a default package to a user whenever a new user is created.
#     """
#     if created:
#         package = Package.objects.get(pk=1)
#         instance.package = package
#         instance.save()
