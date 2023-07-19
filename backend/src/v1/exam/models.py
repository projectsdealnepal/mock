from django.db import models, IntegrityError, transaction
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from v1.question.models import Question, Solution, ExamType, AnswerChoices
from django.utils import timezone


# Create your models here.


class StatusChoices(models.TextChoices):
    PENDING = "P", "PENDING"
    IN_PROGRESS = "I", "IN PROGRESS"
    COMPLETED = "C", "COMPLETED"


class UserExamType(models.Model):
    user = models.ForeignKey(
        "accounts.CustomUser",
        verbose_name=_("user"),
        related_name="user_exam_types",
        on_delete=models.CASCADE,
    )
    exam_type = models.ForeignKey(
        "question.ExamType",
        verbose_name=_("exam type"),
        related_name="user_exam_types",
        on_delete=models.CASCADE,
    )
    enrolled_package = models.ForeignKey(
        "package.package",
        verbose_name=_("package"),
        related_name="user_exam_types",
        null=True,
        on_delete=models.SET_NULL,
    )
    created_date = models.DateTimeField(_("created date"), auto_now_add=True)
    updated_date = models.DateTimeField(_("updated date"), auto_now=True)

    class Meta:
        verbose_name = _("user and exam type")
        verbose_name_plural = _("user and exam types")

    def __str__(self):
        return f"{self.pk} - {self.user.pk} - {self.user.get_full_name()} - Exam {self.exam_type.name}"


class ExamSession(models.Model):
    EXAM_TYPE_SHORT_FORM_LENGTH = 3
    USER_ID_LENGTH = 6
    SESSION_NUMBER_LENGTH = 6

    session_id = models.CharField(_("session id"), unique=True, max_length=31)
    user_exam_type = models.ForeignKey(
        UserExamType,
        verbose_name=_("user exam types"),
        related_name="exam_sessions",
        on_delete=models.CASCADE,
    )

    time_consumed = models.IntegerField(_("time consumed"), null=True)

    created_date = models.DateTimeField(_("created date"), auto_now_add=True)
    updated_date = models.DateTimeField(_("updated date"), auto_now=True)

    status = models.CharField(_("status"), choices=StatusChoices.choices, max_length=1)

    class Meta:
        verbose_name = _("exam session")
        verbose_name_plural = _("exam sessions")

    def __str__(self):
        return self.session_id

    def get_session_id(self):
        user_id = self.user_exam_type.user.pk
        exam_type_Short = self.user_exam_type.exam_type.short_form
        number = str(timezone.now().strftime("%H%M%S"))
        session_id = f"{exam_type_Short}{str(user_id).zfill(self.USER_ID_LENGTH)}{str(number).zfill(self.SESSION_NUMBER_LENGTH)}"
        return session_id

    def save(self, *args, **kwargs):
        if not self.pk:
            self.session_id = self.get_session_id()
        return super().save(self, *args, **kwargs)


class ExamHistory(models.Model):
    exam_session = models.ForeignKey(
        ExamSession,
        verbose_name=_("exam session"),
        related_name="exam_histories",
        on_delete=models.CASCADE,
    )
    exam_date = models.DateTimeField(_("exam date"), auto_now_add=True)
    last_update = models.DateTimeField(_("last updated"), auto_now=True)
    question = models.ForeignKey(
        Question,
        verbose_name=_("question"),
        related_name="exam_histories",
        on_delete=models.CASCADE,
    )
    selected_answer = models.CharField(
        _("selected answer"), null=True, choices=AnswerChoices.choices, max_length=1
    )
    is_correct = models.BooleanField(_("is correct?"), default=False)

    class Meta:
        verbose_name = _("exam history")
        verbose_name_plural = _("exam histories")

    def __str__(self):
        return f"{self.exam_session.user_exam_type.user.get_full_name()} - question {self.question.pk}"


class QuestionHistory(models.Model):
    generated_date = models.DateTimeField(_("generated date"), auto_now_add=False)
    question = models.ForeignKey(
        Question,
        verbose_name=_("question"),
        related_name="question_histories",
        on_delete=models.CASCADE,
    )
    exam_type = models.ManyToManyField(
        ExamType, verbose_name=_("exam type"), related_name="question_histories"
    )
    created_date = models.DateTimeField(_("created date"), auto_now_add=True)
    updated_date = models.DateTimeField(_("updated date"), auto_now=True)

    class Meta:
        verbose_name = _("question history")
        verbose_name_plural = _("question histories")

    def __str__(self):
        return str(self.pk)


class LiveExamSchedule(models.Model):
    exam_date = models.DateTimeField(_("exam date"), auto_now=False, auto_now_add=False)

    class Meta:
        verbose_name = _("Live exam schedule")
        verbose_name_plural = _("Live exam schedule")

    def __str__(self):
        return f"live exam {self.pk} on {self.exam_date}"


class LiveExamRegistration(models.Model):
    exam_schedule = models.ForeignKey(
        LiveExamSchedule,
        verbose_name=_("live exam schedule"),
        related_name="live_exam_registration",
        on_delete=models.CASCADE,
    )
    user_exam_type = models.ForeignKey(
        UserExamType,
        verbose_name=_("user exam type"),
        related_name="live_exam_registration",
        on_delete=models.CASCADE,
    )
    is_booked = models.BooleanField(_("is exam booked"), default=False)
    booked_date = models.DateTimeField(_("exam booked date"), auto_now_add=True)
    status_change_date = models.DateTimeField(
        _("exam booked status change date"), auto_now=True
    )

    class Meta:
        verbose_name = _("live exam registration")
        verbose_name_plural = _("live exam registrations")

    def __str__(self):
        return f"{self.user_exam_type} booked {self.exam_schedule}"


class LiveExamQuestion(models.Model):
    exam_type = models.ForeignKey(
        "question.ExamType",
        verbose_name=_("exam type"),
        related_name="live_exam_question",
        on_delete=models.CASCADE,
    )
    exam_schedule = models.ForeignKey(
        LiveExamSchedule,
        verbose_name=_("live exam schedule"),
        related_name="live_exam_question",
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        "question.Question",
        verbose_name=_("question"),
        related_name="live_exam_question",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("live exam question")
        verbose_name_plural = _("live exam question")

    def __str__(self):
        return f"{self.exam_type} - question - {self.question.pk}"


class liveExamResponse(models.Model):
    user_exam_type = models.ForeignKey(
        "exam.UserExamType",
        verbose_name=_("user exam type"),
        related_name="live_exam_response",
        on_delete=models.CASCADE,
    )
    question = models.ForeignKey(
        LiveExamQuestion,
        verbose_name=_("live exam question"),
        related_name="live_exam_response",
        on_delete=models.CASCADE,
    )
    selected_answer = models.CharField(
        _("selected answer"), null=True, choices=AnswerChoices.choices, max_length=1
    )
    is_correct = models.BooleanField(_("is correct?"), default=False)

    class Meta:
        verbose_name = _("live exam response")
        verbose_name_plural = _("live exam responses")

    def __str__(self):
        return f"{self.user_exam_type} - {self.question}"
