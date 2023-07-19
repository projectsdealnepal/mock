from django.urls import path
from .views import (
    generate_individual_question_list_view,
    user_and_exam_type,
    check_submitted_answer_view,
    exam_session_list_view,
    previous_exam_details_view,
)

# from .views import

app_name = "exam"
urlpatterns = [
    path(
        "individual-question/<int:user_exam_id>",
        generate_individual_question_list_view,
        name="generate_individual_question_list",
    ),
    path(
        "individual-question-answer-submit/",
        check_submitted_answer_view,
        name="check_submitted_answer_view",
    ),
    path("user-exam-type-list/", user_and_exam_type, name="user_and_exam_type"),
    path("exam-session-list/", exam_session_list_view, name="exam_session_list_view"),
    path("previous-exam-details/<str:session_id>", previous_exam_details_view, name="previous_exam_details_view")


    # path('submit-individual-answer/', check_submitted_answer_view, name = 'submit_individual_answer')
]
