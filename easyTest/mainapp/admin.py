from django.contrib import admin
from .models import *


class EditDatabaseAdmin():
    """Edit for root of Database"""
    def get_queryset(self, request):
        return self.model.objects.get_all_queryset()

    def delete_model(self, request, obj):
        """ Given a model instance delete it from the database."""
        obj.hard_delete()

    def delete_queryset(self, request, queryset):
        """Given a queryset, delete it from the database."""
        queryset.hard_delete()


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
    

class ResultAdmin(EditDatabaseAdmin, admin.ModelAdmin):
    fields = ('owner', 'test', 'right_answers_count', 'wrong_answers_count', 'time',  'is_test_passed', 'active', 'sort')
    list_display = ('owner', 'test', 'right_answers_count', 'wrong_answers_count',
                    'get_time',  'is_test_passed', 'active', 'sort', 'deleted')

    def get_time(self, obj):
        return f'{obj.time}'.split('.')[0]
    get_time.short_description = 'Time '


class UserAnswerAdmin(EditDatabaseAdmin, admin.ModelAdmin):
    fields = ('owner', 'result', 'question', 'right_answer', 'user_answer', 'is_correct', 'active')
    list_display = ('owner', 'result', 'question', 'right_answer', 'user_answer', 'is_correct', 'active', 'deleted')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Test, TestAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)
# admin.site.register(TestCategory,TestCategoryAdmin)