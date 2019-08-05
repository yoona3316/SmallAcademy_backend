from django.utils import timezone

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from courses.models import Course

from . import models
from . import nest_serializers as nests


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ('id', 'answer', 'is_answer', )


class NestedAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Answer
        fields = ('id', 'answer', 'is_answer', )
        extra_kwargs = {'id': {'read_only': False}}


class QuestionDefault(object):
    def set_context(self, serializer_field):
        self.question_id = serializer_field.context['question_id']

    def __call__(self, *args, **kwargs):
        return self.question_id


class AnswerAppendSerializer(serializers.ModelSerializer):
    question_id = serializers.HiddenField(default=QuestionDefault())
    class Meta:
        model = models.Answer
        fields = ('id', 'answer', 'is_answer', 'question_id')


class QuizDefault(object):
    def set_context(self, serializer_field):
        self.quiz_id = serializer_field.context['quiz_id']

    def __call__(self):
        return self.quiz_id


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)
    quiz_id = serializers.HiddenField(default=QuizDefault())

    class Meta:
        model = models.Question
        fields = ('id', 'question', 'quiz_id', 'explanation', 'answers')

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        question = models.Question.objects.create(**validated_data)
        for answer_data in answers_data:
            models.Answer.objects.create(question=question, **answer_data)
        return question


class QuestionAllSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)
    quiz_id = serializers.HiddenField(default=QuizDefault())

    class Meta:
        model = models.Quiz
        fields = ('questions', 'quiz_id')

    def update(self, instance, validated_data):
        quiz_id = validated_data.pop('quiz_id')
        for question in validated_data.get('questions'):
            serializer = QuestionSerializer(data=question, context={'quiz_id': quiz_id})
            serializer.is_valid()
            serializer.save()
        return instance



class QuestionDetailSerializer(serializers.ModelSerializer):
    answers = NestedAnswerSerializer(many=True)

    class Meta:
        model = models.Question
        fields = ('id', 'question', 'explanation', 'answers')

    def update(self, instance, validated_data):
        answers_data = validated_data.pop('answers')
        instance.question = validated_data.get('question', instance.question)
        instance.explanation = validated_data.get('explanation', instance.explanation)
        instance.save()
        for answer_data in answers_data:
            answer = models.Answer.objects.get(pk=answer_data.pop('id'))
            serializer = AnswerSerializer(answer, data=answer_data)
            serializer.is_valid()
            serializer.save()
        return instance


class NestedQuestionSerializer(QuestionSerializer):
    answers = NestedAnswerSerializer(many=True)
    class Meta:
        model = models.Question
        fields = ('id', 'question', 'quiz_id', 'explanation', 'answers')
        extra_kwargs = {'id': {'read_only': False}}



class QuizBoxDefault(object):
    def set_context(self, serializer_field):
        self.box_id = serializer_field.context['box_id']

    def __call__(self):
        return self.box_id


class QuizSerializer(serializers.ModelSerializer):
    # questions = serializers.StringRelatedField(many=True)
    quizbox_id = serializers.HiddenField(default=QuizBoxDefault())

    class Meta:
        model = models.Quiz
        fields = ('id', 'title', 'due', 'quizbox_id')

    def create(self, validated_data):
        quiz = super().create(validated_data)
        course_id = quiz.quizbox.course.id
        self.create_grade_for_course_members(quiz, course_id)
        return quiz

    def create_grade_for_course_members(self, quiz, course_id):
        for student in Course.objects.get(pk=course_id).students.all():
            models.Grade.objects.create(quiz=quiz, gradebox=student.gradebox)

    def validate_due(self, value):
        now = timezone.localtime()
        if value < now:
            raise ValidationError("오늘 이후의 날짜로 설정해주십시오.")
        return value

class QuizDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Quiz
        exclude = ('quizbox', 'id', )

class QuizBoxSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    quiz = nests.NestQuizSerializer(many=True, read_only=True)

    class Meta:
        model = models.QuizBox
        fields = ('id', 'course_id', 'course', 'quiz')


class AllStudentGradeSerializer(serializers.ModelSerializer):
    gradebox = serializers.StringRelatedField()
    class Meta:
        model = models.Grade
        fields = '__all__'


class MyGradeSerializer(serializers.ModelSerializer):
    quiz_id = serializers.SlugRelatedField(source='quiz', slug_field='id', read_only=True)
    quiz = serializers.StringRelatedField()

    class Meta:
        model = models.Grade
        fields = ('id', 'grade', 'is_submitted', 'quiz_id', 'quiz', 'gradebox', )


class NestedMyGradeSerializer(serializers.ModelSerializer):
    quiz_id = serializers.SlugRelatedField(source='quiz', slug_field='id', read_only=True)
    quiz = serializers.StringRelatedField()
    course_id = serializers.SlugRelatedField(source='quiz.quizbox.course', slug_field='id', read_only=True)
    course_name = serializers.SlugRelatedField(source='quiz.quizbox.course', slug_field='course_name', read_only=True)

    class Meta:
        model = models.Grade
        fields = ('id', 'grade', 'is_submitted', 'quiz_id', 'quiz', 'gradebox', 'course_id', 'course_name', )


class MyGradeBoxSerializer(serializers.ModelSerializer):
    grades = NestedMyGradeSerializer(many=True, read_only=True)

    class Meta:
        model = models.GradeBox
        fields = ('id', 'user', 'grades',)

# grading 모델을 만든 걸 써야 좋음...!
class GradeQuestionSerializer(serializers.ModelSerializer):
    answers = NestedAnswerSerializer(many=True)

    class Meta:
        model = models.Question
        fields = ('id', 'question', 'answers')
        read_only_fields = ('question', )

    def update(self, instance, validated_data):
        answers = validated_data.get('answers')
        for answer in answers:
            id = answer.get("id")
            is_answer = answer.get("is_answer")
            if not self.grade(id, is_answer):
                raise serializers.ValidationError("Wrong answer!")

        return instance

    def validate_answers(self, value):
        answers = self.instance.answers.all()
        user_answers = value
        for user_answer in user_answers:
            try:
                answers.get(id=user_answer.get('id'))
            except models.Answer.DoesNotExist:
                raise serializers.ValidationError("The selected answer does not exist")
        return value

    def grade(self, id, is_answer):
        return models.Answer.objects.get(id=id).is_answer == is_answer


class NestedGradeQuizSerializer(serializers.ModelSerializer):
    questions = NestedQuestionSerializer(many=True)

    class Meta:
        model = models.Quiz
        fields = ('questions', )


class GradeQuizSerializer(serializers.ModelSerializer):
    quiz = serializers.StringRelatedField()
    is_submitted = serializers.StringRelatedField()
    _quiz = NestedGradeQuizSerializer(source='quiz', write_only=True)
    wrong_answers = NestedQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = models.Grade
        fields = ('id', 'quiz', 'is_submitted', '_quiz', 'grade', 'wrong_answers' )


    def update(self, instance, validated_data):
        grade = 0
        problems = validated_data.pop('quiz').get('questions')
        for problem in problems:
            answers = problem.get('answers')
            if self.correct_answer(answers):
                grade += 1
            else:
                question_id = problem.get('id')
                instance.wrong_answers.add(models.Question.objects.get(pk=question_id))
                instance.save()
        validated_data['grade'] = grade
        validated_data['is_submitted'] = True
        return super().update(instance, validated_data)

    def correct_answer(self, answers):
        for answer in answers:
            id = answer.get('id')
            is_answer = answer.get('is_answer')
            if models.Answer.objects.get(id=id).is_answer != is_answer:
                return False
        return True


class UpcomingQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Quiz
        exclude = ('quizbox', )


class UpcomingQuizAllSerializer(serializers.ModelSerializer):
    course_id = serializers.SlugRelatedField(source='quizbox.course', read_only=True, slug_field='id')
    course_name = serializers.SlugRelatedField(source='quizbox.course', read_only=True, slug_field='course_name')

    class Meta:
        model = models.Quiz
        fields = ('id', 'title', 'due', 'course_id', 'course_name')
