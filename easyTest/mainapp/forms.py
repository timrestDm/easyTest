from django import forms
from django.utils.translation import ugettext_lazy as _
from mainapp.models import Test, TestCategory, Question, Answer
from django.core.exceptions import ValidationError


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ('file', 'title', 'description', 'test_type', 'time', 'required_correct_answers', 'max_questions', 'questions')
        labels = {
            'title': _('Название теста'),
            'description': _('Описание теста'),
            'test_type': _('Тип теста'),
            'time': _('Время теста'),
            'required_correct_answers': _('Правильных ответов для сдачи'),
            'max_questions': _('Макс. количество вопросов в тесте'),
            'questions': _('Вопросы'),
        }

    file = forms.FileField(required=False, label=_('Выберите файл'), help_text='')

    def clean(self):
        """ Check for questions in Test """
        questions = self.cleaned_data.get('questions')
        if not questions:
            raise ValidationError({'questions': _('Необходимо указать хоть один вопрос для теста.')})
        return self.cleaned_data


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
        fields = ('file', 'description', 'q_type')
        labels = {
            'description': _('Вопрос'),
            'q_type': _('Тип вопроса'),
        }
        widgets = {
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 4, 'placeholder': _('Введите текст вопроса')}),
        }

    file = forms.FileField(required=False, label=_('Выберите файл'), help_text='')


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('description', 'is_correct', 'order_number')
        labels = {
            'description': _('Ответ'),
            'is_correct': _('Верный'),
            'order_number': _('Порядковый номер'),
        }
        widgets = {
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 4, 'placeholder': _('Введите текст ответа')}),
        }


AnswerFormSet = forms.inlineformset_factory(Question, Answer, form=AnswerForm, can_delete=False, extra=6)
