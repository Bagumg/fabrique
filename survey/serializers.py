from rest_framework import serializers

from survey.models import Survey, Question, Users, Answer


class SurveySerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance is not None:
            self.fields.get('id').required = True
            self.fields.get('start_date').read_only = True

    class Meta:
        model = Survey
        fields = ('id', 'name', 'start_date', 'end_date', 'description', 'visible')


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('id', 'survey', 'text', 'question_type',)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Users
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = ('user_id', 'question', 'data')

    def create(self, validated_data):
        return Answer.objects.create(**validated_data)
