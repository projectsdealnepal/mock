from django.shortcuts import render, get_object_or_404
from requests import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import (
    ExamTypeSerializer,
    ExamType,
    SolutionSerializer,
    SubjectSerializer,
    TopicSerializer,
    QuestionSerializer,
    DifficultyLevelSerialzer,
    QuestionSolutionSerializer,
)
from rest_framework.views import APIView

from .pagination import QuestionPagination
from .models import ExamType, Question, DifficultyLevel, Subject, Topic, Solution


class DifficultyLevelListView(ListAPIView):
    """
    request type: get

    """

    serializer_class = DifficultyLevelSerialzer
    queryset = DifficultyLevel.objects.all()


difficulty_level_list_view = DifficultyLevelListView.as_view()


class DifficultyLevelDetailsView(RetrieveAPIView):
    serializer_class = DifficultyLevelSerialzer
    queryset = DifficultyLevel.objects.all()


difficulty_level_details_view = DifficultyLevelDetailsView.as_view()


class ExamTypeListView(ListAPIView):
    serializer_class = ExamTypeSerializer
    queryset = ExamType.objects.all()


exam_type_list_view = ExamTypeListView.as_view()


class ExamTypeDetailsView(RetrieveAPIView):
    serializer_class = ExamTypeSerializer
    queryset = ExamType.objects.all()


exam_type_details_view = ExamTypeDetailsView.as_view()


class SubjectListView(ListAPIView):
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()


subject_list_view = SubjectListView.as_view()


class SubjectDetailsView(RetrieveAPIView):
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()


subject_details_view = SubjectDetailsView.as_view()


class TopicListView(ListAPIView):
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()


topic_list_view = TopicListView.as_view()


class TopicDetailsView(RetrieveAPIView):
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()


topic_details_view = TopicDetailsView.as_view()


class QuestionListView(ListAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all().order_by("-id")
    pagination_class = QuestionPagination


question_list_view = QuestionListView.as_view()


class QuestionDetailsView(RetrieveAPIView):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()


question_details_view = QuestionDetailsView.as_view()


class SolutionListView(ListAPIView):
    serializer_class = SolutionSerializer
    queryset = Solution.objects.all()


solution_list_view = SolutionListView.as_view()


class SolutionDetailsView(RetrieveAPIView):
    serializer_class = SolutionSerializer
    queryset = Solution.objects.all()


solution_details_view = SolutionDetailsView.as_view()


class QuestionSolutionListView(ListAPIView):
    serializer_class = QuestionSolutionSerializer
    queryset = Question.objects.all()


question_solution_list_view = QuestionSolutionListView.as_view()


class QuestionSolutionDetailsView(RetrieveAPIView):
    serializer_class = QuestionSolutionSerializer
    queryset = Question.objects.all()


question_solution_details_view = QuestionSolutionDetailsView.as_view()
