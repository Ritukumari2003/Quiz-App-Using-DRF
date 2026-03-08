from django.contrib import admin

from .models import Answer, Question, Quiz

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]

# Register your models here.
admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)