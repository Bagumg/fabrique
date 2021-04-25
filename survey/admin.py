from django.contrib import admin

from survey.models import Survey, Question, Answer, Users


class SurveyAdmin(admin.ModelAdmin):
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['start_date', ]
        else:
            return []


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Users)

