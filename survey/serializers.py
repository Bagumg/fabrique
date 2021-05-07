from rest_framework import serializers

from survey.models import Survey, Question, Users, Answer


class SurveySerializer(serializers.ModelSerializer):

    class Meta:
        model = Survey
        fields = ('name', 'start_date', 'end_date', 'description', 'visible')


class QuestionSerializer(serializers.ModelSerializer):
    # survey = SurveySerializer()

    class Meta:
        model = Question
        fields = ('survey', 'text', 'question_type',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = '__all__'

    def create(self, validated_data):
        return Answer.objects.create(**validated_data)
