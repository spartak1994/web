from django.contrib import admin
from qa.models import QuestionManager, Question, Answer

# Register your models here.
admin.site.register(QuestionManager)
admin.site.register(Question)
admin.site.register(Answer)