from v1.question.models import (
    Subject,
    Topic,
    Question,
    DifficultyLevel,
    QuestionAttachment,
    solutionAttachment,
    Solution,
    ExamType,
)
import random
from django.core.exceptions import ObjectDoesNotExist

exam_types = {
    "Engineering": "ENG",
    "Medical": "MED",
    "Nursing": "NUR",
    "Computer Science and Information Technology": "CSIT",
    "GRE": "GRE",
    "GMAT": "GMAT",
}


for name, short_form in exam_types.items():
    try:
        ExamType.objects.get(name=name)
        print(f"Exam type '{name}' already exists.")
    except ObjectDoesNotExist:
        exam_type = ExamType(name=name, short_form=short_form)
        exam_type.save()
        print(f"Exam type '{name}' created successfully.")


# topics
t = ["Hydrogen", "Atomic Structure", "Oxidation and Reduction"]
sub = Subject.objects.get(name="CHEMISTRY")
for i in t:
    Topic.objects.create(name=i, subject=sub)


t = ["Function", "Algebra", "Trigonometry", "Coordinate Geometry"]
sub = Subject.objects.get(name="MATHEMATICS")
for i in t:
    Topic.objects.create(name=i, subject=sub)


t = ["Thermodynamcis", "Mechanics", "Optics"]
sub = Subject.objects.get(name="PHYSICS")
for i in t:
    Topic.objects.create(name=i, subject=sub)


# list of questions and attachment
topics = Topic.objects.all()
easy = DifficultyLevel.objects.get(pk=1)
hard = DifficultyLevel.objects.get(pk=2)
diff_list = [easy, hard]
attach_list = [True, False]

for diff in diff_list:
    for attach in attach_list:
        for topic in topics:
            question = r"""This is a sample question for  for  difficulty level with {None if attach else 'no'} attachment. Here is the question
                3. If $\displaystyle \int\sqrt{\frac{\cos^{3}x}{\sin^{11}x}}d\mathrm{x}=-2(\mathrm{A}\tan^{\frac{-9}{2}}x+\mathrm{B}\tan^{\frac{-5}{2}}x)+\mathrm{C}$, then
                """
            topic = topic
            option_a = r"$\displaystyle \mathrm{A}=\frac{1}{9}$ , $\displaystyle \mathrm{B}=\frac{-1}{5}$"
            option_b = r"$\displaystyle \mathrm{A}=\frac{1}{9}, \displaystyle \mathrm{B}=\frac{1}{5}$"
            option_c = r"17. $\text{If } \int x^{13 / 2} \cdot\left(1+x^{5 / 2}\right)^{1 / 2} d x=\mathrm{A}\left(1+x^{5 / 2}\right)^{7 / 2}+\mathrm{B}\left(1+x^{5 / 2}\right)^{5 / 2}+\mathrm{C}\left(1+x^{5 / 2}\right)^{3 / 2} \text{, then}$"
            option_d = r"$\displaystyle \int\frac{dx}{(\sqrt{1+x^{2}}-x)^{n}}(n\neq\pm 1)=\frac{1}{2}(\frac{Z^{n+1}}{n+1}+\frac{Z^{n-1}}{n-1})+\mathrm{C},$ where"
            difficulty_level = diff
            has_attachment = attach
            Question.objects.create(
                question=question,
                topic=topic,
                option_a=option_a,
                option_b=option_b,
                option_c=option_c,
                option_d=option_d,
                difficulty_level=difficulty_level,
                has_attachment=has_attachment,
            )


question_attachment_list = Question.objects.filter(has_attachment=True)

for question_attach in question_attachment_list:
    name = f"path/for/quesiton_id{question_attach.pk}/for/topic/{question_attach.topic.name}"
    QuestionAttachment.objects.create(name=name, question=question_attach)


# Solution and Solution attachment
attach_list = [True, False]
option_list = ["a", "b", "c", "d"]
questions = Question.objects.all()
for question in questions:
    question = question
    correct_answer = random.choice(option_list)
    detailed_answer = f"This is a question {question.id} solution"
    has_attachment = random.choice(attach_list)
    Solution.objects.create(
        question=question,
        correct_answer=correct_answer,
        detailed_answer=detailed_answer,
        has_attachment=has_attachment,
    )

solution_attachment_list = Solution.objects.filter(has_attachment=True)
for question_attach in solution_attachment_list:
    name = f"path/for/solution_id{question_attach.pk}/for/topic/{question_attach.question.topic.name}"
    solutionAttachment.objects.create(name=name, solution=question_attach)


{
    "gender": "m",
    "contact_number": "9841955453",
    "date_of_birth": "2022-04-27",
    "college_name": "abc",
    "college_location": "test",
    "home_city": "test",
    "current_city": "test",
}
