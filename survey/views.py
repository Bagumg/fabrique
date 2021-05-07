from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from survey.models import Survey, Users, Question
from survey.serializers import SurveySerializer, AnswerSerializer, QuestionSerializer


class ActiveSurveysView(APIView):
    """
    View вывода активных опросов
    """

    def get(self, request):
        surveys = Survey.objects.filter(visible=True).all()
        serializer = SurveySerializer(surveys, many=True)
        return Response({'Активные опросы': serializer.data})


class GoSurvey(APIView):
    """
    View прохождения опроса.
    Принимает на вход параметры передаваемые GET, HEAD, OPTIONS запросами:
    survey_id - ID опроса. Возвращает JSON вида {'Текст вопроса': 'Тип вопроса'}
    user_id - ID пользователя системы.
    Возвращает JSON всех вопросов пользователя вида {'Название опроса': 'Вопросы'}
    Если пользователя с user_id не существует, создаёт пользователя с user_id
    и возвращает JSON всех активных опросов с вопросами вида {'Название опроса': 'Вопросы'}
    """

    def get(self, request):
        user_id = request.GET.get('user_id')
        survey_id = request.GET.get('survey_id')
        questions_set = {}
        user_surveys = Users.objects.filter(id=user_id)
        if survey_id:
            surveys = Survey.objects.filter(id=survey_id).first()
            questions = Question.objects.filter(survey=surveys.id).all()
            for question in questions:
                questions_set.update({question.text: question.question_type})
            return Response({surveys.name: questions_set})
        if user_surveys:
            for user in user_surveys:
                for survey in user.survey.all():
                    questions_set.update({survey.name: []})
                    for question in Question.objects.all().filter(survey=survey.id):
                        questions_set[survey.name].append([question.text, question.question_type])

            return Response(questions_set)
        else:
            user = Users.objects.create(id=user_id)
            user.save()
            surveys = Survey.objects.filter(visible=True).all()
            survey_set = {}
            for survey in surveys:
                survey_set.update({survey.name: []})
                for question in Question.objects.all().filter(survey=survey.id):
                    survey_set[survey.name].append([question.text, question.question_type])

            return Response(survey_set)


@api_view(['POST'])
def get_answer(request):
    """
    Принимает ответы на вопросы.
    Функция принимает на вход POST запрос c параметрами
    :param request:
                question - ID вопроса на который отправляется ответ
                data - Содержимое вопроса
    :return: Ответ 201 в случае успешного создания ответа, 409 в случае ошибок
    """
    if request.method == 'POST':
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreateSurvey(APIView):

    def post(self, request):
        if request.method == 'POST':
            serializer = SurveySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_409_CONFLICT)

            return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreateQuestion(APIView):

    def post(self, request):
        if request.method == 'POST':
            serializer = QuestionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_409_CONFLICT)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
