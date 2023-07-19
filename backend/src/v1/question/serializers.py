from rest_framework import serializers
from .models import (
    Question,
    ExamType,
    Subject,
    Topic,
    DifficultyLevel,
    QuestionAttachment,
    Solution,
    solutionAttachment,
)

from tools.site_url import get_site_url

class ExamTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamType
        fields = "__all__"


class QuestionAttachmentSerializer(serializers.ModelSerializer):
    attachment_url = serializers.SerializerMethodField()

    class Meta:
        model = QuestionAttachment
        fields = ("name", "attachment_url")

    def get_attachment_url(self, obj):
        # base_url = self.context["request"].build_absolute_uri("/")
        media_url = get_site_url() + "/media/"
        attachment_url = media_url + obj.name
        return attachment_url


class QuestionSerializer(serializers.ModelSerializer):
    question_attachments = QuestionAttachmentSerializer(many=True, read_only=True)
    marks = serializers.SerializerMethodField(read_only=True)
    topic_id = serializers.SerializerMethodField()
    topic_name = serializers.CharField(source="topic.name")
    subject_name = serializers.CharField(source="topic.subject.name")

    class Meta:
        model = Question
        fields = (
            "id",
            "question",
            "option_a",
            "option_b",
            "option_c",
            "option_d",
            "topic_id",
            "topic_name",
            "subject_name",
            "marks",
            "has_attachment",
            "question_attachments",
        )

    def get_marks(self, obj):
        return 1 if obj.difficulty_level.difficulty_level == DifficultyLevel.EASY else 2

    def get_topic_id(self, obj):
        return obj.topic.id


class SubjectSerializer(serializers.ModelSerializer):
    exam_types = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ("id", "name", "exam_types")

    def get_exam_types(self, obj):
        return [exam_type.name for exam_type in obj.exam_types.all()]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["exam_types"] = self.get_exam_types(instance)
        return representation


class TopicSerializer(serializers.ModelSerializer):
    subject = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = (
            "id",
            "name",
            "subject",
        )

    def get_subject(self, obj):
        return obj.subject.name


class DifficultyLevelSerialzer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = DifficultyLevel
        fields = (
            "id",
            "difficulty_level",
            "name",
        )

    def get_name(self, obj):
        return obj.get_difficulty_level_display()


class SolutionAttachmentSerializer(serializers.ModelSerializer):
    attachment_url = serializers.SerializerMethodField()

    class Meta:
        model = solutionAttachment
        fields = ("name", "attachment_url")

    def get_attachment_url(self, obj):
        # base_url = self.context["request"].build_absolute_uri("/")
        # get_site_url
        media_url = get_site_url() + "/media/"
        attachment_url = media_url + obj.name.replace("\\", "/")
        # return attachment_url
        return attachment_url


class SolutionSerializer(serializers.ModelSerializer):
    solution_attachments = SolutionAttachmentSerializer(many=True, read_only=True)
    question_id = serializers.SerializerMethodField()

    class Meta:
        model = Solution
        fields = (
            "id",
            "question_id",
            "correct_answer",
            "detailed_answer",
            "has_attachment",
            "hint_answer",
            "has_attachment",
            "solution_attachments",
        )

    def get_question_id(self, obj):
        return obj.question.id


class QuestionSolutionSerializer(serializers.ModelSerializer):
    solutions = SolutionSerializer(read_only=True)
    question_attachments = QuestionAttachmentSerializer(many=True, read_only=True)
    marks = serializers.SerializerMethodField(read_only=True)
    topic_id = serializers.SerializerMethodField()
    topic_name = serializers.CharField(source="topic.name")
    subject_name = serializers.CharField(source="topic.subject.name")

    class Meta:
        model = Question
        fields = (
            "id",
            "question",
            "option_a",
            "option_b",
            "option_c",
            "option_d",
            "topic_id",
            "topic_name",
            "subject_name",
            "marks",
            "has_attachment",
            "question_attachments",
            "solutions",

        )

    def get_marks(self, obj):
        return 1 if obj.difficulty_level.difficulty_level == DifficultyLevel.EASY else 2

    def get_topic_id(self, obj):
        return obj.topic.id


    
