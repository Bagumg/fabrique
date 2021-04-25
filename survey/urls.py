from django.urls import path

from survey.views import ActiveSurveysView, GoSurvey, get_answer

urlpatterns = [
    path('getActiveSurveys/', ActiveSurveysView.as_view()),
    path('goSurvey/', GoSurvey.as_view()),
    path('getAnswer/', get_answer),
]
