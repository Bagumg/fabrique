from django.urls import path

from survey.views import ActiveSurveysView, GetSurvey, PostAnswer, CreateSurvey, CreateQuestion, UserGetOrCreate, \
    GetUserAnswers, UpdateSurvey, UpdateQuestion, DeleteSurvey, DeleteQuestion

urlpatterns = [
    path('getActiveSurveys/', ActiveSurveysView.as_view()),
    path('getSurvey/', GetSurvey.as_view()),
    path('getUserOrCreate/', UserGetOrCreate.as_view()),
    path('getUserAnswers/', GetUserAnswers.as_view()),
    path('createAnswer/', PostAnswer.as_view()),
    # Surveys CRUD
    path('createSurvey/', CreateSurvey.as_view()),
    path('updateSurvey/', UpdateSurvey.as_view()),
    path('deleteSurvey/', DeleteSurvey.as_view()),
    # Questions CRUD
    path('createQuestion/', CreateQuestion.as_view()),
    path('updateQuestion/', UpdateQuestion.as_view()),
    path('deleteQuestion/', DeleteQuestion.as_view()),
]
