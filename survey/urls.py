from django.urls import path

from survey.views import ActiveSurveysView, GoSurvey, get_answer, CreateSurvey, CreateQuestion

urlpatterns = [
    path('getActiveSurveys/', ActiveSurveysView.as_view()),
    path('goSurvey/', GoSurvey.as_view()),
    path('getAnswer/', get_answer),
    path('createSurvey/', CreateSurvey.as_view()),
    path('createQuestion/', CreateQuestion.as_view()),
]
