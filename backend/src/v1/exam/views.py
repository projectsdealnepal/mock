from django.shortcuts import render, get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from django.db.models import Q
from django.core.cache import cache


from v1.question.models import (
    ExamType,
    Question,
    DifficultyLevel,
    Subject,
    Topic,
    Solution,
)

import yaml
from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import (
    AnswerSubmissionSerializer,
    GenerateQuestionSerializer,
    PreviousIndividualExamDetailsSerializer,
    UserExamTypeSerializer,
    ExamSessionSerializer,
)

from v1.question.serializers import ExamTypeSerializer
from django.conf import settings
from .models import ExamHistory, ExamSession, UserExamType

from .utils import update_consumed_package

from rest_framework.permissions import IsAuthenticated
from .permissions import (
    DailyExamPerDayPermission,
    DailyExamPermission,
    NoteAvailablePermission,
    QuestionPerTopicLimitPermission,
    SolutionAvailablePermission,
    LiveExamPermission,
    TopicExamPerDayPermission,
    TopicExamPermission,
)


class UserAssociatedExamTypeView(ListAPIView):
    """
    Provides the user associated exam type:
    Available method: Get
    """

    serializer_class = UserExamTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = self.request.user.user_exam_types.all()
        return queryset


user_and_exam_type = UserAssociatedExamTypeView.as_view()


class ExamSessionListView(ListAPIView):
    serializer_class = ExamSessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ExamSession.objects.filter(user_exam_type__user=self.request.user)

        # return self.request.user.user_exam_types.all().exam_sessions.all()


exam_session_list_view = ExamSessionListView.as_view()


class GenerateIndividualQuestionListView(APIView):
    """
    Generate individual question list view generates the question based on the question format provided.
    This api privdes the exam_session which is passed to the /v1/exam/individual-question-answer-submit/ api.

    """

    serializer_class = GenerateQuestionSerializer
    permission_classes = [
        IsAuthenticated,
        DailyExamPermission,
        DailyExamPerDayPermission,
    ]
    yaml_data = None

    def get_user_exam_type(self):
        """
        Retrieve a UserExamType object with the id passed as a URL parameter
        """
        pk = self.kwargs["user_exam_id"]
        return get_object_or_404(UserExamType, pk=pk)

    def get_exam_type(self, *args, **kwargs):
        #  different logic will be provided later
        return "test"

    def get_format_dir(self):
        # Returns the directory where the YAML file containing the question format is located
        self.type = self.get_exam_type
        return (
            settings.BASE_DIR
            / "v1"
            / "exam"
            / "syllabus_marks"
            / f"{self.get_exam_type()}.yaml"
        )

    # def get_yaml_data(self):
    #     if self.yaml_data is None:
    #         with open(self.get_format_dir(), "r") as stream:
    #             self.yaml_data = yaml.safe_load(stream)
    #     return self.yaml_data

    def get_yaml_data(self):
        # Returns the YAML data as a dictionary
        with open(self.get_format_dir(), "r") as stream:
            yaml_data = yaml.safe_load(stream)
        return yaml_data

    def get_subject(self, subject_name):
        # Returns the subject object corresponding to the subject name passed as an argument
        return get_object_or_404(Subject, name=subject_name)

    def get_topic(self, subject, topic_name):
        # Returns the topic object corresponding to the topic name and subject object passed as arguments
        return get_object_or_404(Topic, name=topic_name, subject=subject)

    def get_filter_query(self, topic, question_marks, true_or_false):
        # query that filter the difficulty level and the question is present in the exam history table
        user_exam_id = self.kwargs["user_exam_id"]
        difficulty_inst_list = DifficultyLevel.objects.filter(
            Q(difficulty_level=DifficultyLevel.EASY)
            if question_marks == 1
            else ~Q(difficulty_level=DifficultyLevel.EASY)
        )

        query = Q(topic=topic) & Q(difficulty_level__in=difficulty_inst_list)

        # query to get the non repeating question for the particular user
        user_query = Q(
            exam_histories__exam_session__user_exam_type__pk=user_exam_id
        ) | Q(exam_histories__isnull=True)

        # query to get the only incorrect answer
        if not true_or_false:
            exam_histories_query = Q(exam_histories__is_correct=true_or_false) | Q(
                exam_histories__isnull=True
            )
            # adds all the query together
            query &= exam_histories_query & user_query

        else:
            query &= user_query

        print(query)

        return query

    def get_queryset(self):
        # Create an empty list to store the questions
        questions = []

        # Iterate through each YAML file and extract the data
        for data in self.get_yaml_data():
            # Get the subject object corresponding to the subject name in the YAML file
            subject = self.get_subject(data["subject"].upper())

            # Iterate through each topic in the YAML file and get the corresponding Topic object
            for topic_data in data["topics"]:
                topic = self.get_topic(subject, topic_data["name"].upper())

                # Iterate through each question in the YAML file and get the corresponding Question objects
                for question_data in topic_data["questions"]:
                    # Get the marks and number of questions required for the current question
                    question_marks = question_data["marks"]
                    question_count = question_data["number"]

                    # Filter the questions based on the difficulty level and add them to the list of questions
                    if question_count != 0:
                        # Get a filter query to retrieve questions
                        # get only question from previous that are incorrectly answer by the user
                        query = self.get_filter_query(topic, question_marks, False)

                        # Retrieve a list of questions using the filter query and add them to the list of questions
                        filtered_questions = Question.objects.filter(query).order_by(
                            "?"
                        )[:question_count]

                        # if we are short in the number of question remove the previously incorrect answer
                        # and use all the data from previous question
                        if len(filtered_questions) < question_count:
                            query = self.get_filter_query(topic, question_marks, True)
                            filtered_questions = Question.objects.filter(
                                query
                            ).order_by("?")[:question_count]
                        print(
                            f"for topic - {topic} \nneed {question_count}\ngot{len(filtered_questions)}"
                        )
                        questions.extend(filtered_questions)

        # Print the number of questions retrieved
        print(len(questions))

        # Return the list of questions
        return questions

    def get(self, request, *args, **kwargs):
        user_exam_inst = self.get_user_exam_type()

        # Retrieve a queryset of Question objects using the get_queryset() method
        queryset = self.get_queryset()
        # print(queryset)
        # Create a serializer instance for the queryset retrieved in the previous step
        serializer = self.serializer_class(
            queryset, many=True, context={"request": request}
        )

        # Create an ExamSession object with the "status" attribute set to "P", "time_consumed" attribute set to 0,
        # and "user_exam_type" attribute set to the UserExamType object retrieved in the first step
        exam_session_inst = ExamSession(
            status="P", time_consumed=0, user_exam_type=user_exam_inst
        )

        # Save the ExamSession object to the database
        exam_session_inst.save()

        # Create a list of ExamHistory objects for each question in the queryset retrieved earlier
        exam_history_insts = [
            ExamHistory(exam_session=exam_session_inst, question=question_inst)
            for question_inst in queryset
        ]

        # Save the ExamHistory objects to the database using the bulk_create() method
        ExamHistory.objects.bulk_create(exam_history_insts)

        # Create a dictionary with "exam_session" and "questions" keys, where the "exam_session" value is the
        # session_id attribute of the ExamSession object created earlier, and the "questions" value is the serialized
        # data of the queryset retrieved in the first step
        data = {
            "exam_session": exam_session_inst.session_id,
            "questions": serializer.data,
        }

        # update the service used by the user. this updates the value of user by 1
        update_consumed_package(user_exam_inst, update_type="daily")

        # Return the data dictionary in the response with a status code of 200
        return Response(data, status=status.HTTP_200_OK)


generate_individual_question_list_view = GenerateIndividualQuestionListView.as_view()


class CheckSubmittedAnswerView(APIView):
    """
    This API takes a POST request with the following parameters:
    - exam_session: The ID of the exam session being taken
    - time_consumed: The time spent on the current exam session in seconds
    - question_answer: A list of objects, each containing the following parameters:
      - question_id: The ID of the question being answered
      - selected_option: The option selected by the user ('a', 'b', 'c', or 'd')

    The API returns a JSON response with the following data for the answered question:
    - 204 response code if putch else 201 created if post with additional message
    """

    permission_classes = [IsAuthenticated]

    serializer_class = AnswerSubmissionSerializer

    def verify_and_update_status(self, serializer):
        """
        This method takes a serializer instance and updates the exam session status and history of submitted answers.

        Parameters:
        - serializer: A serializer instance containing the validated data for the answer submission.

        Returns:
        - None
        """

        # Retrieve the validated data from the serializer
        exam_session = serializer.validated_data.get("exam_session")
        time_consumed = serializer.validated_data.get("time_consumed")
        answer_data_list = serializer.validated_data.get("question_answer")

        # Update the status of the exam session
        ExamSession.objects.filter(session_id=exam_session).update(
            time_consumed=time_consumed,
            status="I" if self.request.method == "PUT" else "C",
        )

        # Update the selected answers and correctness status in the exam history for each submitted answer
        for answer_data in answer_data_list:
            solution = Solution.objects.get(question__id=answer_data["question_id"])
            is_correct = (
                True
                if answer_data["selected_option"] == solution.correct_answer
                else False
            )
            ExamHistory.objects.filter(
                exam_session__session_id=exam_session,
                question_id=answer_data["question_id"],
            ).update(
                selected_answer=answer_data["selected_option"], is_correct=is_correct
            )

    def get_error_reponse(self, serializer):
        """
        This method retrieves the error message from a serializer instance.

        Parameters:
        - serializer: A serializer instance containing the error message.

        Returns:
        - A string representing the error message.
        """

        try:
            error = serializer.errors["question_answer"]["error"]
        except (KeyError, IndexError):
            error = "Invalid request"
        except:
            error = serializer.errors
        return error

    def post(self, request, *args, **kwargs):
        """
        This method handles a POST request for submitting answers to a question.

        Parameters:
        - request: The HTTP request object containing the data for the answer submission.

        Returns:
        - A JSON response indicating whether the answer submission was successful or not.
        """

        # Create a new instance of the answer submission serializer using the request data
        serializer = AnswerSubmissionSerializer(
            data=self.request.data, context={"request": request}
        )

        # If the serializer data is valid, update the exam session status and history of submitted answers
        if serializer.is_valid():
            self.verify_and_update_status(serializer)
            data = {"detail": "question and selected answers received successfully"}
            return Response(data, status=status.HTTP_201_CREATED)

        # If the serializer data is invalid, return an error response
        else:
            error = self.get_error_reponse(serializer)
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        """
        This method handles a PATCH request for updating the status of a previously submitted answer.

        Parameters:
        - request: The HTTP request object containing the updated data for the answer submission.

        Returns:
        - A HTTP 204 No Content response with no body if the request is valid and processed successfully.
        - A HTTP 400 Bad Request response with an error message if the request is invalid or fails to process.

        """
        serializer = AnswerSubmissionSerializer(
            data=request.data, context={"request": request}
        )

        # Check if the serializer is valid
        if serializer.is_valid():
            # If it is valid, call the 'verify_and_update_status' method to update the status of the exam session and the answers
            self.verify_and_update_status(serializer)
            # Return a 204 NO CONTENT response indicating success
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            # If the serializer is not valid, get the error response and return it along with a 400 BAD REQUEST response
            error = self.get_error_reponse(serializer)
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)


check_submitted_answer_view = CheckSubmittedAnswerView.as_view()


class PreviousIndividualExamDetailsView(APIView):
    """
    This API view returns the details of a previous individual exam for a given exam session ID.

    Parameters:
    - session_id: The ID of the exam session for which the details are being requested.

    Returns:
    - A JSON response containing the details of the exam session.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = PreviousIndividualExamDetailsSerializer

    def get_queryset(self, session_id):
        """
        This method retrieves the exam session instance for the given session ID.

        Parameters:
        - session_id: The ID of the exam session being queried.

        Returns:
        - An instance of the ExamSession model for the given session ID.
        """
        try:
            exam_session_inst = ExamSession.objects.get(session_id=session_id)
            return exam_session_inst

        except:
            return Response(
                data={"error": f"{session_id} not found"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def get(self, *args, **kwargs):
        """
        This method handles a GET request for retrieving the details of a previous individual exam.

        Returns:
        - A JSON response containing the details of the exam session.
        """
        session_id = self.kwargs["session_id"]
        serializer = self.serializer_class(self.get_queryset(session_id))
        return Response(serializer.data)


previous_exam_details_view = PreviousIndividualExamDetailsView.as_view()
