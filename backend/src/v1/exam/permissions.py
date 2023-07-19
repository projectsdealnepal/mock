from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist

from v1.exam.models import UserExamType


def check_permission(request, user_exam_inst, used_number, total_number):
    if request.user == user_exam_inst.user and total_number >= used_number:
        return True

    if request.user != user_exam_inst.user:
        raise PermissionDenied("You don't have permission to perform this action")

    if total_number < used_number:
        raise PermissionDenied("No remaining exam, please purchase to continue")

    return False


class LiveExamPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_exam_inst = view.get_user_exam_type()
        used_number = user_exam_inst.used_package.used_live_exam
        total_number = user_exam_inst.enrolled_package.live_exam
        return check_permission(request, user_exam_inst, used_number, total_number)


class DailyExamPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_exam_inst = view.get_user_exam_type()
        try:
            used_number = user_exam_inst.used_package.used_daily_exam
            total_number = user_exam_inst.enrolled_package.daily_exam
        except ObjectDoesNotExist:
            raise PermissionDenied(
                "You are not subscribed to any package, please purchase to continue"
            )
        except:
            raise PermissionDenied(
                "You do not have permission, please contact support. "
            )

        return check_permission(request, user_exam_inst, used_number, total_number)


class DailyExamPerDayPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_exam_inst = view.get_user_exam_type()
        try:
            used_number = user_exam_inst.used_package.used_daily_exam_per_day

            total_number = user_exam_inst.enrolled_package.daily_exam_per_day
        except ObjectDoesNotExist:
            raise PermissionDenied(
                "You are not subscribed to any package, please purchase to continue"
            )
        except:
            raise PermissionDenied(
                "You do not have permission, please contact support. "
            )
        return check_permission(request, user_exam_inst, used_number, total_number)


class TopicExamPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_exam_inst = view.get_user_exam_type()
        try:
            used_number = user_exam_inst.used_package.used_topic_exam
            total_number = user_exam_inst.enrolled_package.topic_exam
        except ObjectDoesNotExist:
            raise PermissionDenied(
                "You are not subscribed to any package, please purchase to continue"
            )
        except:
            raise PermissionDenied(
                "You do not have permission, please contact support. "
            )
        return check_permission(request, user_exam_inst, used_number, total_number)


class TopicExamPerDayPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user_exam_inst = view.get_user_exam_type()
            used_number = user_exam_inst.used_package.used_topic_exam_per_day
            total_number = user_exam_inst.enrolled_package.topic_exam_per_day
        except ObjectDoesNotExist:
            raise PermissionDenied(
                "You are not subscribed to any package, please purchase to continue"
            )
        except:
            raise PermissionDenied(
                "You do not have permission, please contact support. "
            )
        return check_permission(request, user_exam_inst, used_number, total_number)


class QuestionPerTopicLimitPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user_exam_inst = view.get_user_exam_type()
            used_number = user_exam_inst.used_package.used_question_per_topic
            total_number = user_exam_inst.enrolled_package.question_per_topic
        except ObjectDoesNotExist:
            raise PermissionDenied(
                "You are not subscribed to any package, please purchase to continue"
            )
        except:
            raise PermissionDenied(
                "You do not have permission, please contact support. "
            )
        return check_permission(request, user_exam_inst, used_number, total_number)


class SolutionAvailablePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_exam_inst = view.get_user_exam_type()
        if user_exam_inst.enrolled_package.is_solution_available:
            return True
        return False


class NoteAvailablePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user_exam_inst = view.get_user_exam_type()
        if user_exam_inst.enrolled_package.is_note_available:
            return True
        return False
