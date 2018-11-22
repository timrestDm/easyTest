from django import forms
from django.utils.translation import ugettext_lazy as _
from mainapp.models import Test, TestCategory, Question, Answer, Group, Student
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, UserChangeForm


class TestForm(forms.ModelForm):
    '''Класс формы создания теста'''

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
        cleaned_data = super().clean()
        file = cleaned_data.get('file')

        if file:
            if file.name.split('.')[-1] == 'json':
                return self.cleaned_data
            else:
                raise ValidationError({'file':_('Загрузите файл в верном формате.')})

        if cleaned_data.get('title') == '':
            raise ValidationError({'title': _('Название теста не должно быть пустым.')})
        if cleaned_data.get('time') is None or cleaned_data.get('time') == 0:
            raise ValidationError({'time': _('Необходимо указать время теста.')})
        if cleaned_data.get('required_correct_answers') is None or cleaned_data.get('required_correct_answers') < 1:
            raise ValidationError({'required_correct_answers': _('Необходимо указать корректное кол-во правильных ответов для сдачи.')})
        if cleaned_data.get('max_questions') is None or cleaned_data.get('max_questions') < 1:
            raise ValidationError({'max_questions': _('Необходимо указать корректное максимальное кол-во ответов.')})
        if not cleaned_data.get('questions'):
            raise ValidationError({'questions': _('Необходимо указать хоть один вопрос для теста.')})

        return self.cleaned_data


class TestCategoryForm(forms.ModelForm):
    '''Класс формы создания категории'''

    class Meta:
        model = TestCategory
        fields = ('title', 'description', 'cat')
        labels = {
            'title': _('Название категории'),
            'description': _('Описание категории'),
            'cat': _('Подкатегория'),
        }


class QuestionForm(forms.ModelForm):
    '''Класс формы создания вопроса'''

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
    '''Класс формы создания ответа'''

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