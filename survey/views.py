from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from survey.models import Survey, Users, Question, Answer
from survey.serializers import SurveySerializer, AnswerSerializer, QuestionSerializer, UserSerializer


class ActiveSurveysView(APIView):
    """
    View вывода активных опросов
    """

    def get(self, request):
        surveys = Survey.objects.filter(visible=True).all()
        serializer = SurveySerializer(surveys, many=True)
        return Response({'Активные опросы': serializer.data})


class GetSurvey(APIView):
    """
    View прохождения опроса.
    Принимает на вход параметры передаваемые GET запросом:
    survey_id - ID опроса. Возвращает JSON вида {'Текст вопроса': 'Тип вопроса'}
    Возвращает JSON всех вопросов пользователя вида {'Название опроса': 'Вопросы'}
    Если пользователя с user_id не существует, создаёт пользователя с user_id
    и возвращает JSON всех активных опросов с вопросами вида {'Название опроса': 'Вопросы'}
    """

    def get(self, request):
        survey_id = request.data.get('survey_id')
        questions_set = {}
        if survey_id:
            surveys = Survey.objects.filter(id=survey_id).first()
            questions = Question.objects.filter(survey=surveys.id).all()
            for question in questions:
                questions_set.update({question.text: (question.question_type, question.id)})
            return Response({surveys.name: questions_set})
        else:
            surveys = Survey.objects.filter(visible=True).all()
            serializer = SurveySerializer(surveys, many=True)
            return Response([r'Missing required field survey_id. Available Surveys:', serializer.data],
                            status=status.HTTP_400_BAD_REQUEST)


class UserGetOrCreate(APIView):
    """
    Endpoint создания пользователя.
    Если пользователь существует, возвращает ID этого пользователя
    """

    def get(self, request):
        user_id = request.data.get('user_id')
        try:
            user = Users.objects.create(id=user_id)
            user.save()
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            user = Users.objects.get(id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)


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


# @api_view(['POST'])
# def post_answer(request):
#     """
#     Принимает ответы на вопросы.
#     Функция принимает на вход POST запрос c параметрами
#     :param request:
#                 question - ID вопроса на который отправляется ответ
#                 data - Содержимое вопроса
#     :return: Ответ 201 в случае успешного создания ответа, 409 в случае ошибок
#     """
#     if request.method == 'POST':
#         serializer = AnswerSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         else:
#             return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

class PostAnswer(APIView):

    def post(self, request):
        if request.method == 'POST':
            serializer = AnswerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
            return Response(serializer.data, status=status.HTTP_201_CREATED)



# @api_view(['GET'])
# def get_user_answers(request):
#     if request.method == 'GET':
#         answers = Answer.objects.all()
#         data = []
#         for answer in answers:
#             if answer.user_id.id == request.data.get('user_id'):
#                 data.append([
#                     {"ID опроса": answer.question.survey.id},
#                     {"Опрос": answer.question.survey.name},
#                     {"ID вопроса": answer.question.id},
#                     {"Тип вопроса": answer.question.question_type},
#                     {"Вопрос": answer.question.text},
#                     {"Ответ": answer.data}])
#         return Response(data)


class GetUserAnswers(APIView):

    def get(self, request):
        if request.method == 'GET':
            answers = Answer.objects.all()
            data = []
            for answer in answers:
                if answer.user_id.id == request.data.get('user_id'):
                    data.append([
                        {"ID опроса": answer.question.survey.id},
                        {"Опрос": answer.question.survey.name},
                        {"ID вопроса": answer.question.id},
                        {"Тип вопроса": answer.question.question_type},
                        {"Вопрос": answer.question.text},
                        {"Ответ": answer.data}])
            return Response(data, status=status.HTTP_200_OK)
