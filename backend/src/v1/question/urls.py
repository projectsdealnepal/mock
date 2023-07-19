from django.urls import path
from .views import (
    exam_type_list_view,
    exam_type_details_view,
    question_list_view,
    question_details_view,
    subject_list_view,
    solution_details_view,
    topic_list_view,
    topic_details_view,
    difficulty_level_list_view,
    difficulty_level_details_view,
    solution_list_view,
    subject_details_view,
    question_solution_list_view,
    question_solution_details_view,

    
)

app_name = "question"
urlpatterns = [
    path("exam-type-list/", exam_type_list_view, name="exam_type_list"),
    path(
        "exam-type-details/<int:pk>/", exam_type_details_view, name="exam_type_details"
    ),
    path("question-list/", question_list_view, name="question_list"),
    path("question-details/<int:pk>/", question_details_view, name="question_details"),
    path("subject-list/", subject_list_view, name="subject_list"),
    path("subject-details/<int:pk>/", subject_details_view, name="subject_details"),
    path("topic-list/", topic_list_view, name="topic_list"),
    path("topic-details/<int:pk>/", topic_details_view, name="topic_details"),
    path("solution-list/", solution_list_view, name="solution_list"),
    path("solution-details/<int:pk>/", solution_details_view, name="solution_details"),
    path(
        "difficulty-level-list/",
        difficulty_level_list_view,
        name="difficulty_level_list",
    ),
    path(
        "difficulty-level-details/<int:pk>/",
        difficulty_level_details_view,
        name="difficulty_level_details",
    ),
    path(
        "question-solution-list/",
        question_solution_list_view,
        name="question_solution_list_view",
    ),
    path(
        "question-solution-details/<int:pk>/",
        question_solution_details_view,
        name="question_solution_details_view",
    ),
]
