from django.apps import AppConfig


class QuestionConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "v1.question"

    def ready(self) -> None:
        return super().ready()