from django import forms
from django.utils.translation import ugettext_lazy as _
from mainapp.models import Test, TestCategory, Question, Answer


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ('title', 'description', 'test_type', 'time', 'required_correct_answers', 'max_questions', 'questions')
        labels = {
            'title': _('Название теста'),
            'description': _('Описание теста'),
            'test_type': _('Тип теста'),
            'time': _('Время теста'),
            'required_correct_answers': _('Правильных ответов для сдачи'),
            'max_questions': _('Макс. количество вопросов в тесте'),
            'questions': _('Вопросы'),
        }


class TestCategoryForm(forms.ModelForm):
    class Meta:
        model = TestCategory
        fields = ('title', 'description', 'cat')
        labels = {
            'title': _('Название категории'),
            'description': _('Описание категории'),
            'cat': _('Подкатегория'),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('description',)
        labels = {
            'description': _('Вопрос'),
        }
        widgets = {
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 2, 'placeholder': _('Введите текст вопроса')}),
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('description', 'is_correct')
        labels = {
            'description': _('Ответ'),
            'is_correct': _('Верный'),
        }
        widgets = {
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 2, 'placeholder': _('Введите текст ответа')}),
        }


AnswerFormSet = forms.inlineformset_factory(Question, Answer, form=AnswerForm, can_delete=False, extra=6)
