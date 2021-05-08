from django.urls import path

from survey.views import ActiveSurveysView, GetSurvey, PostAnswer, CreateSurvey, CreateQuestion, UserGetOrCreate, \
    GetUserAnswers

urlpatterns = [
    path('getActiveSurveys/', ActiveSurveysView.as_view()),
    path('getSurvey/', GetSurvey.as_view()),
    path('getUserOrCreate/', UserGetOrCreate.as_view()),
    # path('getUserAnswers/', get_user_answers),
    path('getUserAnswers/', GetUserAnswers.as_view()),
    # path('createAnswer/', post_answer),
    path('createAnswer/', PostAnswer.as_view()),
    path('createSurvey/', CreateSurvey.as_view()),
    path('createQuestion/', CreateQuestion.as_view()),
]
