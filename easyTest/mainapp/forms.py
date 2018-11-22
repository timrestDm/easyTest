from django import forms
from django.utils.translation import ugettext_lazy as _
from mainapp.models import Test, TestCategory, Question, Answer, Group, Student
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


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


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('title', 'description', 'parent_group',)
        labels = {
            'title': _('Название группы'),
            'description': _('Описание'),
            'parent_group': _('Родительская группа'),
        }


class StudentForm(UserCreationForm):
    class Meta:
        model = Student
        fields = ('username', 'first_name', 'group', 'password1', 'password2', 'email',)
        labels = {
            'username': _('Логин'),
            'first_name': _('ФИО'),
            'group': _('Группа'),
            'password1': _('Пароль'),
            'password2': _('Повтор пароля'),
            'email': _('email'),
        }


class StudentEditForm(UserChangeForm):
    class Meta:
        model = Student
        fields = ('username', 'first_name', 'group', 'email', 'password')
        labels = {
            'username': _('Логин'),
            'first_name': _('ФИО'),
            'group': _('Группа'),
            'password': _('Пароль'),
            'email': _('email'),
        }

    def __init__(self, *args, **kwargs):
        super(StudentEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.help_text = ''
            if field_name == 'password':
                field.widget = forms.HiddenInput()