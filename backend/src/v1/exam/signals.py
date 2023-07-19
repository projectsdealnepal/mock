from django.dispatch import receiver
from django.db.models.signals import post_save

from v1.package.models import Package
from v1.exam.models import UserExamType


@receiver(post_save, sender=UserExamType)
def assign_default_package(sender, instance, created, **kwargs):
    """
    This signal function assigns a default package to a user whenever a new user update its profile.
    """
    if created:
        package = Package.objects.get(pk=1)
        instance.enrolled_package = package
        instance.save()
