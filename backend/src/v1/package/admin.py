from django.contrib import admin

from .models import Package, UsedPackage


class PackageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "daily_exam",
        "topic_exam",
        "live_exam",
        "question_per_topic",
        "topic_exam_per_day",
        "daily_exam_per_day",
        "is_solution_available",
        "is_note_available",
        "created_date",
        "updated_date",
    )
    search_fields = ("name",)
    list_filter = ("is_solution_available", "is_note_available")
    date_hierarchy = "created_date"


class UsedPackageAdmin(admin.ModelAdmin):
    list_display = (
        "user_exam_type",
        "used_daily_exam",
        "used_topic_exam",
        "used_live_exam",
        "used_question_per_topic",
        "used_topic_exam_per_day",
        "used_daily_exam_per_day",
        "is_solution_available",
        "is_note_available",
        "created_date",
        "updated_date",
    )
    search_fields = ("user_exam_type__user__username",)
    list_filter = (
        "is_solution_available",
        "is_note_available",
        "user_exam_type__enrolled_package__name",
    )
    date_hierarchy = "created_date"


admin.site.register(Package, PackageAdmin)
admin.site.register(UsedPackage, UsedPackageAdmin)
