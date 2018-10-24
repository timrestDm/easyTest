from django.contrib import admin
from .models import Question, Answer, TestCategory, Test


# class KeywordAdmin(admin.ModelAdmin):
#     fields = ('title', 'active', 'sort')
# admin.site.register(Keyword,KeywordAdmin)


class AnswerInline(admin.TabularInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'keyword', 'active', 'sort')
    inlines = [
        AnswerInline,
    ]


class AnswerAdmin(admin.ModelAdmin):
    fields = ('title', 'description', 'question', 'is_correct', 'active', 'sort')


# class TestCategoryAdmin(admin.ModelAdmin):
#     fields = ('title', 'description', 'active', 'sort')


# class TestAdmin(admin.ModelAdmin):
#     fields = ('title', 'description','keywords',  'category', 'max_questions', 'required_correct_answers', 'active', 'sort')



admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer,AnswerAdmin)
# admin.site.register(Test,TestAdmin)
# admin.site.register(TestCategory,TestCategoryAdmin)