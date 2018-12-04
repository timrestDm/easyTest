from django import forms
from django.utils.translation import ugettext_lazy as _
from mainapp.models import Test, TestCategory, Question, Answer, Group, Student
from django.core.exceptions import ValidationError
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import transaction
import commentjson


class MutualWidget:
    """Класс для добавления общих виджетов для форм"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = ''
            if field_name != 'file':
                field.widget.attrs['class'] = 'form-control'


class TestForm(MutualWidget, forms.ModelForm):
    """Класс формы создания теста"""

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
            'questions': _('Добавьте вопросы в тест'),
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'questions': FilteredSelectMultiple(verbose_name=None, is_stacked=False),
        }

    class Media:
        css = {'all': ('/static/admin/css/widgets.css',), }
        js = ('/admin/jsi18n/',)

    file = forms.FileField(required=False, label=_('Загрузить'), help_text='')

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        queryset = type(self).Meta.model.questions.rel.model.objects.get_questions(request)
        setattr(self.fields['questions'], 'queryset', queryset)

    def clean(self, request=None):
        """ Check for questions in Test """
        cleaned_data = super().clean()
        file = cleaned_data.get('file')

        if file:
            if request:
                if file.name.split('.')[-1] == 'json':
                    try:
                        try:
                            json_string = file.read().decode("utf-8-sig")
                        except:
                            self.add_error('file', _('Файл должен быть в кодировке UTF-8'))
                        else:
                            test = commentjson.loads(json_string)
                            question_model = self.Meta.model.questions.rel.model
                            answer_model = question_model.answers.rel.related_model

                            with transaction.atomic():
                                    questions = test.pop('questions', None)
                                    instance = self.Meta.model.objects.get_or_create(title=test['title'],
                                                                                     owner=request.user)[0]
                                    self.Meta.model.objects.filter(pk=instance.pk).update(**test)
                                    instance.questions.clear()
                                    questions_list = []
                                    for question in questions:
                                        answers = question.pop('answers', None)
                                        obj = question_model.objects.get_or_create(**question, owner=request.user)[0]
                                        if answers:
                                            obj.answers.all().hard_delete()
                                            for answer in answers:
                                                answer_model.objects.create(**answer, question=obj)
                                        questions_list.append(obj)
                                    instance.questions.add(*questions_list)

                    except:
                        self.add_error('file', _('Проверьте правильность ввода данных в json.'))
                else:
                    self.add_error('file', _('Файл должен быть в формате json.'))
            return self.cleaned_data

        if cleaned_data.get('title') == '':
            self.add_error('title', _('Название теста не должно быть пустым.'))
        if cleaned_data.get('time', 0) == 0:
            self.errors.pop('time')
            self.add_error('time', _('Необходимо задать время для прохождения теста.'))
        if cleaned_data.get('required_correct_answers', 0) < 1:
            self.add_error('required_correct_answers', _('Необходимо задать количество правильных ответов для сдачи.'))
        if cleaned_data.get('required_correct_answers', 0) > cleaned_data.get('max_questions', 0):
            self.add_error('required_correct_answers', _('Не должно быть больше максимального количества вопросов'))
        if cleaned_data.get('max_questions', 0) < 1:
            self.add_error('max_questions', _('Необходимо задать максимальное количество вопросов.'))
        if not cleaned_data.get('questions'):
            self.add_error('questions', _('Необходимо задать минимум один вопрос для теста.'))

        return self.cleaned_data


class TestCategoryForm(forms.ModelForm):
    """Класс формы создания категории"""

    class Meta:
        model = TestCategory
        fields = ('title', 'description', 'cat')
        labels = {
            'title': _('Название категории'),
            'description': _('Описание категории'),
            'cat': _('Подкатегория'),
        }


class QuestionForm(MutualWidget, forms.ModelForm):
    """Класс формы создания вопроса"""

    class Meta:
        model = Question
        fields = ('description', 'q_type')
        labels = {
            'description': _('Вопрос'),
            'q_type': _('Тип вопроса'),
        }
        widgets = {
            'description': forms.Textarea(attrs={'cols': 50, 'rows': 4, 'placeholder': _('Введите текст вопроса')}),
        }

    def clean(self):
        """ Check for questions in QuestionForm """
        cleaned_data = super().clean()
        if not cleaned_data.get('description'):
            self.add_error('description', 'Введите вопрос')
        return self.cleaned_data


class AnswerForm(MutualWidget, forms.ModelForm):
    """Класс формы создания ответа"""

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


class AnswerInlineFormSet(forms.BaseInlineFormSet):
    """Класс для вывода форм ответов рядом с вопросами"""

    def clean(self):
        valid_answers = [True for i in self.cleaned_data if i.get('description')]
        if self.data['q_type'] == 'select':
            valid_is_correct = [True for i in self.cleaned_data if i.get('description') and i.get('is_correct')]
        elif self.data['q_type'] == 'sort':
            order_numbers = [i['order_number'] for i in self.cleaned_data if i.get('order_number') is not None]
            valid_is_correct = True if len(valid_answers) == len(set(order_numbers)) and len(valid_answers) != 0 else False

        if not valid_answers:
            self._non_form_errors.data.append('Ни одного ответа не задано.')
        if not valid_is_correct:
            if type(valid_is_correct) == list:
                self._non_form_errors.data.append('Не выбран правильный ответ.')
            else:
                self._non_form_errors.data.append('Не определен порядок ответов.')

        if self._non_form_errors:
            raise ValidationError(self._non_form_errors.data)

        return self.cleaned_data


AnswerFormSet = forms.inlineformset_factory(Question, Answer, form=AnswerForm, formset=AnswerInlineFormSet, 
                                            can_delete=False, extra=6)

                                            
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('title', 'parent_group', 'description', 'tests')
        labels = {
            'title': _('Название группы'),
            'description': _('Описание'),
            'parent_group': _('Родительская группа'),
            'tests': _('Выберите тесты'),
        }


class StudentForm(MutualWidget, UserCreationForm):
    class Meta:
        model = Student
        fields = ('username', 'first_name', 'in_groups', 'password1', 'password2', 'email',)
        labels = {
            'username': _('Логин'),
            'first_name': _('ФИО'),
            'in_groups': _('Группа'),
            'password1': _('Пароль'),
            'password2': _('Повтор пароля'),
            'email': _('email'),
        }


class StudentEditForm(MutualWidget, UserChangeForm):
    class Meta:
        model = Student
        fields = ('username', 'first_name', 'in_groups', 'email', 'password')
        labels = {
            'username': _('Логин'),
            'first_name': _('ФИО'),
            'in_groups': _('Группа'),
            'password': _('Пароль'),
            'email': _('email'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()

