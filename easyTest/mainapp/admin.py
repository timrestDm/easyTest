from django.contrib import admin
from .models import *


# class KeywordAdmin(admin.ModelAdmin):
#     fields = ('title', 'active', 'sort')
# admin.site.register(Keyword,KeywordAdmin)


class AnswerInline(admin.TabularInline):
    model = Answer
    exclude = ('title',)
    
class QuestionAdmin(admin.ModelAdmin):
    fields = ('description', 'active', 'sort')
    inlines = [AnswerInline,]


class AnswerAdmin(admin.ModelAdmin):
    fields = ('description', 'question', 'is_correct', 'active', 'sort')


# class TestCategoryAdmin(admin.ModelAdmin):
#     fields = ('title', 'description', 'active', 'sort')


class TestAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'owner', 'questions', 'keywords',  'category', 'max_questions',
              'required_correct_answers', 'active', 'sort')
    list_display = ('title', 'owner',  'category', 'max_questions', 'required_correct_answers', 'active', 'sort')
    

class ResultAdmin(admin.ModelAdmin):
    fields = ('owner', 'test', 'right_answers_count', 'wrong_answers_count', 'time',  'is_test_passed', 'active', 'sort')
    list_display = ('owner', 'test', 'right_answers_count', 'wrong_answers_count',
                    'get_time',  'is_test_passed', 'active', 'sort')

    def get_time(self, obj):
        return f'{obj.time}'.split('.')[0]
    get_time.short_description = 'Time '



admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Result, ResultAdmin)
# admin.site.register(TestCategory,TestCategoryAdmin)