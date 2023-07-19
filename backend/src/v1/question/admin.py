from django.contrib import admin
from .models import (
    DifficultyLevel,
    ExamType,
    QuestionAttachment,
    Subject,
    Topic,
    Question,
    Solution,
    Notes,
    solutionAttachment,
)


@admin.register(DifficultyLevel)
class DifficultyLevelAdmin(admin.ModelAdmin):
    list_display = ("id", "get_difficulty_level_display")


@admin.register(ExamType)
class ExamTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "short_form")


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    filter_horizontal = ("exam_types",)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "subject")
    list_filter = ("subject",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "topic", "difficulty_level", "has_attachment")
    list_filter = ("topic__subject", "difficulty_level", "topic__name")
    search_fields = ("question",)


@admin.register(QuestionAttachment)
class QuestionAttachmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "question")


@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_display_str",
        "question",
        "correct_answer",
        "has_attachment",
    )
    list_filter = ("question__topic__subject",)


@admin.register(solutionAttachment)
class SolutionAttachmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "solution")


@admin.register(Notes)
class NotesAdmin(admin.ModelAdmin):
    list_display = ("id", "note", "topic", "has_attachment")
    list_filter = ("topic__subject",)
