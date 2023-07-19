from django.db import models
from django.utils.translation import gettext_lazy as _
from v1.exam.models import UserExamType

# Create your models here.


class Package(models.Model):
    name = models.CharField(_("package name"), max_length=50)
    daily_exam = models.IntegerField(_("no of daily exam"))
    topic_exam = models.IntegerField(_("no of topic exam"))
    live_exam = models.IntegerField(_("no of live exam"))
    question_per_topic = models.IntegerField(_("no of question per topic"))
    topic_exam_per_day = models.IntegerField(_("no of topic exam per day"))
    daily_exam_per_day = models.IntegerField(_("no of daily exam per day"))
    is_solution_available = models.BooleanField(
        _("is solution available "), default=False
    )
    is_note_available = models.BooleanField(_("is note available"), default=False)
    created_date = models.DateTimeField(_("created date"), auto_now_add=True)
    updated_date = models.DateTimeField(_("updated date"), auto_now=True)

    class Meta:
        verbose_name = _("package")
        verbose_name_plural = _("packages")

    def __str__(self):
        return self.name


class UsedPackage(models.Model):
    user_exam_type = models.OneToOneField(
        UserExamType,
        verbose_name=_("user exam type"),
        related_name="used_package",
        on_delete=models.CASCADE,
    )
    used_daily_exam = models.IntegerField(_("used no of daily exam"))
    used_topic_exam = models.IntegerField(_("used no of topic exam"))
    used_live_exam = models.IntegerField(_("used no of live exam"))
    used_question_per_topic = models.IntegerField(_("used no of question per topic"))
    used_topic_exam_per_day = models.IntegerField(_("used no of topic exam per day"))
    used_daily_exam_per_day = models.IntegerField(_("used no of daily exam per day"))
    is_solution_available = models.BooleanField(
        _("is solution available "), default=False
    )
    is_note_available = models.BooleanField(_("is note available"), default=False)
    created_date = models.DateTimeField(_("created date"), auto_now_add=True)
    updated_date = models.DateTimeField(_("updated date"), auto_now=True)

    class Meta:
        verbose_name = _("used package")
        verbose_name_plural = _("used packages")

    def __str__(self):
        return f"{ self.user_exam_type.pk } - { self.user_exam_type.enrolled_package}"
