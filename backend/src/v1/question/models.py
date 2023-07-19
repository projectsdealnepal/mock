from django.db import models, IntegrityError
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import IntegrityError


class AnswerChoices(models.TextChoices):
    A = "a", "Option A"
    B = "b", "Option B"
    C = "c", "Option C"
    D = "d", "Option D"


class DifficultyLevel(models.Model):
    VERY_EASY = 1
    EASY = 2
    MEDIUM = 3
    HARD = 4
    VERY_HARD = 5
    COMPLEX = 6
    IMPOSSIBLE = 7

    LEVEL_CHOICES = (
        (VERY_EASY, _("Very Easy")),
        (EASY, _("Easy")),
        (MEDIUM, _("Medium")),
        (HARD, _("Hard")),
        (VERY_HARD, _("Very Hard")),
        (COMPLEX, _("Complex")),
        (IMPOSSIBLE, _("Impossible")),
    )

    difficulty_level = models.IntegerField(choices=LEVEL_CHOICES, default=EASY)
    created_date = models.DateTimeField(_("created date"), auto_now_add=True)
    updated_date = models.DateTimeField(_("updated date"), auto_now=True)

    class Meta:
        verbose_name = _("Difficulty level")
        verbose_name_plural = _("Difficulty levels")

    def __str__(self):
        return self.get_difficulty_level_display()

    def get_absolute_url(self):
        return reverse("question:difficulty_level_detail", kwargs={"pk": self.pk})


class ProductType(models.Model):
    """
    types are live exam, Daily exam, topic wise exam
    """

    name = models.CharField(_("name"), max_length=50)
    created_date = models.DateTimeField(_("created date"), auto_now_add=True)
    updated_date = models.DateTimeField(_("updated date"), auto_now=True)

    class Meta:
        verbose_name = _("Product type")
        verbose_name_plural = _("Product types")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("question:product_type_detail", kwargs={"pk": self.pk})


class ExamType(models.Model):
    """
    types are Engineering, Medical, Nursing etc
    """

    name = models.CharField(_("name"), unique=True, max_length=60)
    short_form = models.CharField(_("short name"), unique=True, max_length=4)
    created_date = models.DateTimeField(_("created date"), auto_now_add=True)
    updated_date = models.DateTimeField(_("updated date"), auto_now=True)

    class Meta:
        verbose_name = _("Exam type")
        verbose_name_plural = _("Exam types")

    def __str__(self):
        return self.name

    def generate_short_form(self):
        """
        Generate a short form based on the first three characters of the name
        """
        return self.name[:4].upper()

    def save(self, *args, **kwargs):
        if not self.short_form:
            self.short_form = self.generate_short_form()
        self.short_form = self.short_form.upper()
        self.name = self.name.upper()

        try:
            return super().save(*args, **kwargs)
        except IntegrityError:
            existing_data = ExamType.objects.get(name=self.name)
            self.id = existing_data.id
            return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("question:exam_type_detail", kwargs={"pk": self.pk})


class Subject(models.Model):
    name = models.CharField(_("subject"), max_length=100, unique=True)
    exam_types = models.ManyToManyField(
        ExamType, verbose_name=_("exam types"), related_name="subjects"
    )
    created_date = models.DateTimeField(_("created date"), auto_now_add=True)
    updated_date = models.DateTimeField(_("updated date"), auto_now=True)

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            self.name = self.name.upper()
            return super().save(*args, **kwargs)
        except IntegrityError:
            self.name = self.name.upper()
            existing_data = Subject.objects.get(name=self.name)
            self.id = existing_data.id
            return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("question:subject_detail", kwargs={"pk": self.pk})


class Topic(models.Model):
    name = models.CharField(_("name"), max_length=100, unique=True)
    subject = models.ForeignKey(
        Subject,
        verbose_name=_("subject"),
        related_name="topics",
        on_delete=models.CASCADE,
    )
    created_date = models.DateTimeField(_("created date"), auto_now_add=True)
    updated_date = models.DateTimeField(_("updated date"), auto_now=True)

    class Meta:
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            self.name = self.name.upper()
            return super().save(*args, **kwargs)
        except IntegrityError:
            self.name = self.name.upper()
            existing_topic = Topic.objects.get(name=self.name)
            self.id = existing_topic.id
            return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("question:topic_detail", kwargs={"pk": self.pk})


class Question(models.Model):
    topic = models.ForeignKey(
        Topic,
        verbose_name=_("topic"),
        related_name="questions",
        on_delete=models.CASCADE,
    )
    question = models.TextField(_("question"))
    option_a = models.CharField(_("option a"), max_length=500)
    option_b = models.CharField(_("option b"), max_length=500)
    option_c = models.CharField(_("option c"), max_length=500)
    option_d = models.CharField(_("option d"), max_length=500)
    difficulty_level = models.ForeignKey(
        DifficultyLevel,
        verbose_name=_("difficulty level"),
        related_name="questions",
        null=True,
        blank=True,
        default=DifficultyLevel.EASY,
        on_delete=models.SET_NULL,
    )
    has_attachment = models.BooleanField(_("has attachment"))
    created_date = models.DateTimeField(_("created date"), auto_now_add=True)
    updated_date = models.DateTimeField(_("updated date"), auto_now=True)

    class Meta:
        verbose_name = _("question")
        verbose_name_plural = _("questions")

    def __str__(self):
        return f"{self.pk}_{self.question[:50]}"

    def get_absolute_url(self):
        return reverse("question:question_detail", kwargs={"pk": self.pk})


class Solution(models.Model):
    question = models.OneToOneField(
        Question,
        verbose_name=_("question"),
        related_name="solutions",
        on_delete=models.CASCADE,
    )
    correct_answer = models.CharField(
        _("correct answer"), choices=AnswerChoices.choices, max_length=1
    )
    detailed_answer = models.TextField(_("detail answer"), null=True, blank=True)
    has_attachment = models.BooleanField(_("has attachment"))
    created_date = models.DateTimeField(_("created date"), auto_now_add=True)
    updated_date = models.DateTimeField(_("updated date"), auto_now=True)
    hint_answer = models.TextField(_("solution hint"), null=True, blank=True)

    class Meta:
        verbose_name = _("solution")
        verbose_name_plural = _("solutions")

    def __str__(self):
        return self.get_display_str()

    def get_display_str(self):
        return f"{self.question.question[:10]}_{self.question.pk}_{self.correct_answer}"

    def get_absolute_url(self):
        return reverse("question:solution_detail", kwargs={"pk": self.pk})


class Notes(models.Model):
    note = models.TextField(_("note"))
    topic = models.ForeignKey(
        Topic, verbose_name=_("topic"), related_name="notes", on_delete=models.CASCADE
    )

    has_attachment = models.BooleanField(_("has attachment"))
    created_date = models.DateTimeField(_("created date"), auto_now_add=True)
    updated_date = models.DateTimeField(_("updated date"), auto_now=True)

    class Meta:
        verbose_name = _("notes")
        verbose_name_plural = _("notes")

    def __str__(self):
        return {self.topic.name} - {self.note[:50]}

    def get_absolute_url(self):
        return reverse("question:notes_detail", kwargs={"pk": self.pk})


class QuestionAttachment(models.Model):
    name = models.CharField(_("name"), max_length=120)
    question = models.ForeignKey(
        Question,
        verbose_name=_("question"),
        related_name="question_attachments",
        on_delete=models.CASCADE,
    )
    created_date = models.DateTimeField(_("created date"), auto_now_add=True)
    updated_date = models.DateTimeField(_("updated date"), auto_now=True)

    class Meta:
        verbose_name = _("question attachment")
        verbose_name_plural = _("question attachments")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("question:question_attachment_detail", kwargs={"pk": self.pk})


class NoteAttachment(models.Model):
    name = models.CharField(_("name"), max_length=120)
    note = models.ForeignKey(
        Notes,
        verbose_name=_("note"),
        related_name="note_attachments",
        on_delete=models.CASCADE,
    )
    created_date = models.DateTimeField(_("created date"), auto_now_add=True)
    updated_date = models.DateTimeField(_("updated date"), auto_now=True)

    class Meta:
        verbose_name = _("note attachment")
        verbose_name_plural = _("note attachments")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("question:note_attachment_detail", kwargs={"pk": self.pk})


class solutionAttachment(models.Model):
    name = models.CharField(_("name"), max_length=120)
    solution = models.ForeignKey(
        Solution,
        verbose_name=_("solution"),
        related_name="solution_attachments",
        on_delete=models.CASCADE,
    )
    created_date = models.DateTimeField(_("created date"), auto_now_add=True)
    updated_date = models.DateTimeField(_("updated date"), auto_now=True)

    class Meta:
        verbose_name = _("solution attachment")
        verbose_name_plural = _("solution attachments")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("question:solution_attachment_detail", kwargs={"pk": self.pk})
