from rest_framework import serializers
from v1.question.models import Question, DifficultyLevel, AnswerChoices
from v1.question.serializers import (
    QuestionAttachmentSerializer,
    QuestionSolutionSerializer,
)
from .models import ExamHistory, UserExamType, ExamSession
from drf_spectacular.utils import extend_schema_field


class UserExamTypeSerializer(serializers.ModelSerializer):
    exam_type_name = serializers.CharField(source='exam_type.name')
    
    class Meta:
        model = UserExamType
        fields = (
            "id",
            "user",
            "exam_type",
            "exam_type_name",
        )



class ExamSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamSession
        fields = '__all__'


class GenerateQuestionSerializer(serializers.ModelSerializer):
    topic_name = serializers.CharField(source="topic.name", read_only=True)
    subject_name = serializers.CharField(source="topic.subject.name", read_only=True)
    marks = serializers.SerializerMethodField(read_only=True)
    question_attachments = QuestionAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = (
            "id",
            "question",
            "option_a",
            "option_b",
            "option_c",
            "option_d",
            "topic",
            "topic_name",
            "subject_name",
            "marks",
            "difficulty_level",
            "has_attachment",
            "question_attachments",
        )
    
    @extend_schema_field(int)
    def get_marks(self, obj):
        return 1 if obj.difficulty_level.difficulty_level == DifficultyLevel.EASY else 2



class AnswerSubmitSerializer(serializers.Serializer):
    question_id = serializers.IntegerField()
    selected_option = serializers.ChoiceField(choices=AnswerChoices.choices)

    class Meta:
        fields = (
            "question_id",
            "selected_option",
        )


class ExamHistorySerializer(serializers.ModelSerializer):
    # question_details = QuestionSolutionSerializer(many=True)
    class Meta:
        model = ExamHistory
        fields = "__all__"


class AnswerSubmissionSerializer(serializers.Serializer):
    exam_session = serializers.CharField(max_length=31)
    time_consumed = serializers.IntegerField()
    # question_answer = AnswerSubmitSerializer(many=True)

    question_answer = serializers.ListSerializer(child=AnswerSubmitSerializer())

    def validate_question_answer(self, data):
        """
        Custom validator method to validate each user answer
        """
        response_data = {
            'error': None,
        }
        try:
            exam_session = self.context['request'].data['exam_session']
            ExamSession.objects.get(session_id=exam_session)
        except ExamSession.DoesNotExist:
            response_data['error']= f'exam session {exam_session} does not exist.'
            raise serializers.ValidationError(response_data)

        # Check that each question_id is valid
        question_ids = [d['question_id'] for d in data]

        valid_question_ids = Question.objects.filter(
            exam_histories__exam_session__session_id=exam_session
        ).values_list("id", flat=True)
        invalid_question_ids = set(question_ids) - set(valid_question_ids)

        if invalid_question_ids:
            response_data['error']= f"Invalid question IDs: {list(invalid_question_ids)}"
            raise serializers.ValidationError(response_data)

        return data



class ExamHistoryResponseSerializer(serializers.ModelSerializer):
    question_details = QuestionSolutionSerializer(source="question")
    selected_answer = serializers.CharField()
    is_correct = serializers.CharField()

    class Meta:
        model = ExamHistory
        fields = (
            "question_details",
            "selected_answer",
            "is_correct",
        )


class PreviousIndividualExamDetailsSerializer(serializers.ModelSerializer):
    exam_date = serializers.SerializerMethodField()
    question_data = serializers.SerializerMethodField()
    class Meta:
        model = ExamSession
        fields = (
            "session_id",
            "user_exam_type",
            "time_consumed",
            "status",
            "exam_date",
            "question_data"
        )

    def get_exam_date(self, obj):
        return obj.exam_histories.last().exam_date
    
    def get_question_data(self, obj):
        query_set = obj.exam_histories.all()
        return ExamHistoryResponseSerializer(
                query_set,
                many=True,
            ).data