from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from survey.models import Survey, Users, Question, Answer
from survey.serializers import SurveySerializer, AnswerSerializer, QuestionSerializer, UserSerializer


class ActiveSurveysView(APIView):
    """
    Endpoint вывода активных опросов
    :return
        JSON вида: {'Активные опросы': список активных опросов}
    """

    @swagger_auto_schema(
        tags=['Получение списка активных опросов'],
        operation_id='Active surveys',
        operation_description='Получение списка активных опросов',
    )
    def get(self, request):
        surveys = Survey.objects.filter(visible=True).all()
        serializer = SurveySerializer(surveys, many=True)
        return Response({'Активные опросы': serializer.data})


class GetSurvey(APIView):
    """
    Endpoint прохождения опроса.
    Принимает на вход параметр:
    survey_id: id опроса.
    :return
        JSON вида {'Текст вопроса': 'Тип вопроса'}
    """

    @swagger_auto_schema(
        tags=['Прохождение опроса'],
        operation_id='Take a survey',
        operation_description='Прохождение опроса',
        responses={
            '200': 'OK',
            '400': 'Bad request'
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'survey_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id опроса'),
            }
        )
    )
    def post(self, request):
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
    Принимает на вход параметр:
    :param
        user_id: id пользователя
    :return
        JSON вида {'id': user_id}
        Если пользователь уже существует, возвращает ID этого пользователя
        Если передаётся пустое поле создаёт нового пользователя
    """

    @swagger_auto_schema(
        tags=['Создание пользователя'],
        operation_id='Create user',
        operation_description='Создание пользователя',
        responses={
            '200': 'OK',
            '201': 'Created'
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id пользователя'),
            }
        )
    )
    def post(self, request):
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
    """
    Endpoint создания опроса
    POST запрос на создание опроса.
    Принимает на вход параметры:
    :param
        name: название опроса
        start_date: дата начала опроса формата YYYY-MM-DD
        end_date: дата окончания опроса формата YYYY-MM-DD
        description: описание опроса
        visible: активен опрос или нет
    :return
        JSON вида {
                name: название опроса,
                start_date: дата начала опроса формата YYYY-MM-DD,
                end_date: дата окончания опроса формата YYYY-MM-DD,
                description: описание опроса,
                visible: активен опрос или нет,
            }
    """

    @swagger_auto_schema(
        tags=['Создание опроса'],
        operation_id='Create survey',
        operation_description='Создание опроса',
        responses={
            '201': 'Created',
            '409': 'Conflict'
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Название опроса'),
                'start_date': openapi.Schema(type=openapi.TYPE_STRING, description='Дата старта формата YYYY-MM-DD'),
                'end_date': openapi.Schema(type=openapi.TYPE_STRING, description='Дата окончания формата YYYY-MM-DD'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Описание опроса'),
                'visible': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Активен или нет'),
            }
        )
    )
    def post(self, request):
        if request.method == 'POST':
            serializer = SurveySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_409_CONFLICT)

            return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateSurvey(APIView):
    """
    Endpoint редактирования опроса
    PATCH запрос на редактирование опроса.
    Принимает на вход параметры:
    :param
        name: название опроса
        start_date: дата начала опроса формата YYYY-MM-DD
        end_date: дата окончания опроса формата YYYY-MM-DD
        description: описание опроса
        visible: активен опрос или нет
    :return
        JSON вида {
                name: название опроса,
                start_date: дата начала опроса формата YYYY-MM-DD,
                end_date: дата окончания опроса формата YYYY-MM-DD,
                description: описание опроса,
                visible: активен опрос или нет,
            }
    """

    @swagger_auto_schema(
        tags=['Редактирование опроса'],
        operation_id='Update survey',
        operation_description='Редактирование опроса',
        responses={
            '201': 'Created',
            '409': 'Conflict'
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'survey_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id опроса'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Название опроса'),
                'end_date': openapi.Schema(type=openapi.TYPE_STRING, description='Дата окончания формата YYYY-MM-DD'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Описание опроса'),
                'visible': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Активен или нет'),
            }
        )
    )
    def patch(self, request):
        survey = Survey.objects.get(id=request.data['survey_id'])
        serializer = SurveySerializer(survey, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


class DeleteSurvey(APIView):
    """
    Endpoint удаления запроса
    DELETE запрос с параметром:
    :param
        survey_id: id опроса
    """

    @swagger_auto_schema(
        tags=['Удаление опроса'],
        operation_id='Delete survey',
        operation_description='Удаление опроса',
        responses={
            '204': 'No content',
            '404': 'Not found'
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'survey_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id опроса'),
            }
        )
    )
    def delete(self, request):
        try:
            survey = Survey.objects.get(id=request.data['survey_id'])
        except Exception as e:
            survey = None
        if survey:
            survey.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CreateQuestion(APIView):
    """
    Endpoint создания вопроса.
    Принимает на вход параметры:
    :param
        survey: id опроса
        text: текст вопроса
        question_type: тип вопроса (
                        TEXT: ответ текстом,
                        SELECT: ответ с выбором одного варианта,
                        SELECT_MULTIPLE: ответ с выбором нескольких вариантов)
    :return
        JSON вида {
                'survey': id опроса,
                'text': текст вопроса,
                'question_type': тип вопроса
            }
    """

    @swagger_auto_schema(
        tags=['Создание вопроса'],
        operation_id='Create question',
        operation_description='Создание вопроса',
        responses={
            '201': 'Created',
            '409': 'Conflict'
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'survey': openapi.Schema(type=openapi.TYPE_STRING, description='id опроса'),
                'text': openapi.Schema(type=openapi.TYPE_STRING, description='Текст вопроса'),
                'question_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Тип вопроса ('
                                'TEXT: ответ текстом, '
                                'SELECT: ответ с выбором одного варианта, '
                                'SELECT_MULTIPLE: ответ с выбором нескольких вариантов)'),
            }
        )
    )
    def post(self, request):
        if request.method == 'POST':
            serializer = QuestionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateQuestion(APIView):
    """
    Endpoint редактирования вопроса.
    Принимает на вход параметры:
    :param
        question_id: id вопроса
        survey: id опроса
        text: текст вопроса
        question_type: тип вопроса (
                        TEXT: ответ текстом,
                        SELECT: ответ с выбором одного варианта,
                        SELECT_MULTIPLE: ответ с выбором нескольких вариантов)
    :return
        JSON вида {
                'id': id вопроса
                'survey': id опроса,
                'text': текст вопроса,
                'question_type': тип вопроса
            }
    """

    @swagger_auto_schema(
        tags=['Редактирование вопроса'],
        operation_id='Update question',
        operation_description='Редактирование вопроса',
        responses={
            '201': 'Created',
            '409': 'Conflict'
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'question_id': openapi.Schema(type=openapi.TYPE_STRING, description='id опроса'),
                'survey': openapi.Schema(type=openapi.TYPE_STRING, description='id опроса'),
                'text': openapi.Schema(type=openapi.TYPE_STRING, description='Текст вопроса'),
                'question_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description='Тип вопроса ('
                                'TEXT: ответ текстом, '
                                'SELECT: ответ с выбором одного варианта, '
                                'SELECT_MULTIPLE: ответ с выбором нескольких вариантов)'),
            }
        )
    )
    def patch(self, request):
        question = Question.objects.get(id=request.data['question_id'])
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_409_CONFLICT)


class DeleteQuestion(APIView):
    """
    Endpoint удаления вопроса
    DELETE запрос с параметром:
    :param
        question_id: id вопроса
    """
    @swagger_auto_schema(
        tags=['Удаление вопроса'],
        operation_id='Delete question',
        operation_description='Удаление вопроса',
        responses={
            '204': 'No content',
            '404': 'Not found'
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'question_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id вопроса'),
            }
        )
    )

    def delete(self, request):
        try:
            question = Question.objects.get(id=request.data['question_id'])
        except Exception as e:
            question = None
        if question:
            question.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class PostAnswer(APIView):
    """
    Endpoint отправки ответа.
    Принимает на вход параметры:
    :param
        question: вопроса
        data: данные ответа
        user_id: id пользователя
    :return
            {
                'question': id вопроса,
                'data': данные ответа,
                'user_id': id пользователя,
            }
    """

    @swagger_auto_schema(
        tags=['Отправка ответа'],
        operation_id='Create answer',
        operation_description='Прием ответа',
        responses={
            '201': 'Created',
            '409': 'Conflict'
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'question': openapi.Schema(type=openapi.TYPE_STRING, description='id вопроса'),
                'data': openapi.Schema(type=openapi.TYPE_STRING, description='Данные ответа'),
                'user_id': openapi.Schema(type=openapi.TYPE_STRING, description='id пользователя'),
            }
        )
    )
    def post(self, request):
        if request.method == 'POST':
            serializer = AnswerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_409_CONFLICT)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class GetUserAnswers(APIView):
    """
    Endpoint получения ответов пользователя.
    Принимает на вход параметр:
    :param
        user_id: id пользователя
    :return
        JSON вида {
            [
                        {"ID опроса": опроса},
                        {"Опрос": текст опроса},
                        {"ID вопроса": id вопроса},
                        {"Тип вопроса": тип вопроса},
                        {"Вопрос": текст вопроса},
                        {"Ответ": ответ пользователя}
            ]
        }
    """

    @swagger_auto_schema(
        tags=['Получение ответов пользователя'],
        operation_id='Get user answers',
        operation_description='Получение ответов пользователя',
        responses={
            '200': 'OK',
        },
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='id пользователя'),
            }
        )
    )
    def post(self, request):
        if request.method == 'POST':
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
