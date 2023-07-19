from v1.package.models import Package, UsedPackage


def update_consumed_package(user_exam_type, update_type=None):
    user_package_inst = UsedPackage.objects.get(user_exam_type=user_exam_type)
    if update_type == "daily":
        user_package_inst.used_daily_exam += 1
        user_package_inst.used_daily_exam_per_day += 1

    elif update_type == "topic":
        user_package_inst.used_topic_exam += 1
        user_package_inst.used_topic_exam_per_day += 1
        user_package_inst.used_question_per_topic += 1

    elif update_type == "live":
        user_package_inst.used_live_exam += 1

    else:
        pass

    user_package_inst.save()
