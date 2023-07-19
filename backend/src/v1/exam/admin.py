from django.contrib import admin
from .models import ExamHistory, QuestionHistory, ExamSession, UserExamType
from django.db.models import Q
from django import forms


# Register your models here.
@admin.register(ExamHistory)
class ExamHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "exam_session",
        "exam_date",
        "question_id",
        "selected_answer",
        "is_correct",
    )
    list_filter = ("exam_date",)


@admin.register(QuestionHistory)
class QuestionHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "generated_date",
    )
    list_filter = ("exam_type",)


class UserExamTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "exam_type")
    list_filter = ("exam_type__name",)
    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "exam_type__name",
    )

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        if search_term:
            queryset = queryset.filter(
                Q(user__email__icontains=search_term)
                | Q(user__first_name__icontains=search_term)
                | Q(user__last_name__icontains=search_term)
                | Q(exam_type__name__icontains=search_term)
            )
        return queryset, use_distinct


admin.site.register(UserExamType, UserExamTypeAdmin)


class ExamSessionAdminForm(forms.ModelForm):
    class Meta:
        model = ExamSession
        exclude = ("session_id",)


class ExamSessionAdmin(admin.ModelAdmin):
    form = ExamSessionAdminForm

    list_display = (
        "session_id",
        "user_exam_type",
        "status",
        "created_date",
        "updated_date",
        "time_consumed",
    )
    list_filter = (
        "user_exam_type__exam_type__name",
        "status",
        "created_date",
        "updated_date",
        "time_consumed",
    )
    search_fields = (
        "session_id",
        "user_exam_type__user__email",
        "user_exam_type__user__first_name",
        "user_exam_type__user__last_name",
        "user_exam_type__exam_type__name",
    )

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        if search_term:
            queryset = queryset.filter(
                Q(session_id__icontains=search_term)
                | Q(user_exam_type__user__email__icontains=search_term)
                | Q(user_exam_type__user__first_name__icontains=search_term)
                | Q(user_exam_type__user__last_name__icontains=search_term)
                | Q(user_exam_type__exam_type__name__icontains=search_term)
            )
        return queryset, use_distinct


admin.site.register(ExamSession, ExamSessionAdmin)
