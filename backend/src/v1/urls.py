# v1/urls.py
from django.urls import path, include

urlpatterns = [
    path("question/", include("v1.question.urls"), name="question"),
    path("exam/", include("v1.exam.urls"), name="exam"),
    path("package/", include("v1.package.urls"), name="package"),
]
