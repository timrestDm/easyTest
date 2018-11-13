from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic.base import RedirectView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from .models import *
import datetime
from django.core.exceptions import PermissionDenied
from mainapp.forms import TestForm, TestCategoryForm, QuestionForm, AnswerFormSet


class StaffPassesTestMixin(UserPassesTestMixin):
    """Миксин делает проверку пользователя на принадлежность к персоналу""" 
    raise_exception = True

    def test_func(self):
        return self.request.user.is_staff


class MainView(TemplateView):
    """Класс отображает главную страницу"""
    template_name = 'mainapp/index.html'


class UsersRedirectView(RedirectView):
    """Класс для автологина пользователей admin или test при нажатии на соответствующую ссылку"""
    pattern_name = 'mainapp:main'

    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs['slug']
        user = authenticate(username=slug, password=slug)
        login(self.request, user)
        return super().get_redirect_url()


class QuestionList(LoginRequiredMixin, ListView):
    """docstring for test"""
    model = Question
    login_url = reverse_lazy('authapp:login')
    paginate_by = 1

    def get_queryset(self):
        return self.model.objects.get_test_questions(self.request, self.kwargs['pk'])


class QuestionCreate(StaffPassesTestMixin, CreateView):
    """Класс создания вопроса с ответами"""
    model = Question
    form_class = QuestionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answers'] = AnswerFormSet()
        context['error_messages'] = self.kwargs.get('error_messages')
        if context['error_messages']:
            context['answers'] = AnswerFormSet(self.request.POST)
        return context

    def form_valid(self, form):
        formset = AnswerFormSet(self.request.POST)

        valid_question = form.cleaned_data.get('description')
        valid_answer = [True for i in formset.cleaned_data if i.get('description')]
        valid_is_correct = [True for i in formset.cleaned_data if i.get('description') and i.get('is_correct')]
        self.kwargs['error_messages'] = []
        if not valid_question:
            self.kwargs['error_messages'].append('Не введен вопрос.')
        if not valid_answer:
            self.kwargs['error_messages'].append('Ни одного ответа не задано.')
        if not valid_is_correct:
            self.kwargs['error_messages'].append('Не выбран правильный ответ.')
        if self.kwargs.get('error_messages'):
            return self.form_invalid(form)

        formset.instance = form.save()
        return super().form_valid(formset)

    def get_success_url(self):
        return reverse_lazy('mainapp:main')


class TestTimeIsOver(LoginRequiredMixin, ListView):
    template_name = 'mainapp/test_time_is_over.html'
    model = Question


class TestList(LoginRequiredMixin, ListView):
    model = Test
    login_url = reverse_lazy('authapp:login')


class StaffTestList(StaffPassesTestMixin, ListView):
    """Класс для просмотра всех созданных тестов пользователем"""
    model = Test
    template_name = 'mainapp/tests_staff_list.html'

    def get_queryset(self):
        return self.model.objects.get_tests(self.request)


class TestCreate(StaffPassesTestMixin, CreateView):
    """Класс создания нового теста"""
    model = Test
    form_class = TestForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class TestEditView(StaffPassesTestMixin, UpdateView):
    """Класс изменения теста"""
    form_class = TestForm
    model = Test

    def get_success_url(self):
        return reverse_lazy('mainapp:tests_staff')

class TestDeleteView(StaffPassesTestMixin, DeleteView):
    """Класс удаления теста"""
    model = Test
    
    def get_success_url(self):
        if self.model.objects.filter(owner=self.request.user).count() == 1:
            return reverse_lazy('mainapp:main')
        else:
            return reverse_lazy('mainapp:tests_staff')


class TestCategoryCreate(StaffPassesTestMixin, CreateView):
    model = TestCategory
    form_class = TestCategoryForm

    def get_success_url(self):
        return reverse_lazy('mainapp:testcategory_list')


class TestCategoryList(StaffPassesTestMixin, ListView):
    """Класс для просмотра всех созданных тестов пользователем"""
    model = TestCategory
    template_name = 'mainapp/testscategory_list.html'


class TestCategoryDelete(StaffPassesTestMixin, DeleteView):
    """Класс удаления теста"""
    model = TestCategory
    success_url = reverse_lazy('mainapp:main')


class ResultCreate(CreateView):
    """docstring for ResultCreate"""
    fields = '__all__'
    model = Result
    slug_url_kwarg = slug_field = 'test'

    def get_success_url(self):
        return reverse_lazy('mainapp:test', kwargs={'pk': self.kwargs['test']})

    def form_valid(self, form):
        Result.objects.get_result_test_queryset(self.request, self.kwargs['test']).hard_delete()
        self.request.session['test_time_begin'] = datetime.datetime.now().timestamp()
        
        form.instance.owner = self.request.user
        form.instance.test = form.fields[self.slug_field].to_python(self.kwargs[self.slug_url_kwarg])
        response = super().form_valid(form)

        self.request.session['test_time'] = datetime.time.strftime(self.object.test.time, '%M:%S')
        self.kwargs['pk'] = self.kwargs['test']
        for question in QuestionList(request=self.request, args=self.args, kwargs=self.kwargs).get_queryset():
            self.kwargs['question'] = question
            self.kwargs['result'] = self.object
            UserAnswerCreate.as_view()(self.request, *self.args, **self.kwargs)

        return response


class ResultList(LoginRequiredMixin, ListView):
    model = Result
    login_url = reverse_lazy('authapp:login')

    def get_queryset(self):
        return self.model.objects.get_results(self.request)


class ResultDetail(LoginRequiredMixin, DetailView):
    """docstring for ResultDetail"""
    model = Result
    slug_field = 'owner'
    login_url = reverse_lazy('authapp:login')

    def get_object(self):
        self.kwargs[self.slug_url_kwarg] = self.request.user
        que = Result.objects.get_result_test_queryset(self.request, self.kwargs['test'])
        response = super().get_object(queryset=que)
        return response

    def get_context_data(self, **kwargs):
        context = {}
        if self.object:
            context['object'] = self.object
            context['user_incorrect_answers'] = self.object.user_answers.get_incorrect_answers()
        context.update(kwargs)
        return super().get_context_data(**context)


class ResultUpdate(ResultDetail, UpdateView):
    """docstring for ResultUpdate"""
    fields = ('right_answers_count', 'wrong_answers_count',)

    def get_object(self):
        response = super().get_object()
        if not response:
            ResultCreate.as_view()(self.request, *self.args, **self.kwargs)
            response = super().get_object()
        self.kwargs['result'] = response
        return response

    def form_valid(self, form):
        self.success_url = self.request.POST['href']
        self.request.session['test_time'] = self.request.POST['left_time']

        if form.instance.active:
            return super().form_valid(form)

        time_result = (datetime.datetime.utcnow() - datetime.timedelta(seconds=self.request.session['test_time_begin'])).time()
        if time_result > self.object.test.time:
            return HttpResponseRedirect(reverse_lazy('mainapp:test_time_is_over', kwargs={'test': self.kwargs['test']}))

        if self.request.POST.get('answer_id'):
            answer = Answer.objects.get(pk=self.request.POST['answer_id'])
        else:
            answer = ''
            self.success_url = self.request.POST['href_current']

        self.kwargs['answer'] = answer
        self.kwargs['question'] = Question.objects.get(pk=self.request.POST['question_id'])

        UserAnswerUpdate.as_view()(self.request, *self.args, **self.kwargs)

        if self.success_url.startswith('/result'):
            form.instance.active = True
            form.instance.time = time_result
            form.instance.right_answers_count = len(self.object.user_answers.get_correct_answers())
            form.instance.wrong_answers_count = len(self.object.user_answers.get_incorrect_answers())

            if form.instance.right_answers_count >= self.object.test.required_correct_answers:
                form.instance.is_test_passed = True

        response = super().form_valid(form)
        return response


class UserAnswerCreate(CreateView):
    """docstring for UserAnswer Create"""
    fields = '__all__'
    model = UserAnswer

    def form_valid(self, form):
        self.success_url = self.request.POST.get('href', '/')

        form.instance.owner = self.request.user
        form.instance.question = self.kwargs['question']
        form.instance.result = self.kwargs['result']

        return super().form_valid(form)


class UserAnswerUpdate(UpdateView):
    """docstring for UserAnswer Update"""
    fields = ('right_answer', 'user_answer', 'is_correct')
    model = UserAnswer
    slug_field = 'owner'

    def get_object(self):
        self.kwargs[self.slug_url_kwarg] = self.request.user
        que = UserAnswer.objects.get_queryset_from_question(self.kwargs['question'], self.kwargs['test'])
        try:
            response = super().get_object(queryset=que)
        except:
            UserAnswerCreate.as_view()(self.request, *self.args, **self.kwargs)
            response = super().get_object(queryset=que)
        return response

    def form_valid(self, form):
        self.success_url = self.request.POST['href']

        form.instance.right_answer = str(self.object.question.answers.get_correct_answer())
        form.instance.user_answer = str(self.kwargs['answer'])
        form.instance.is_correct = True if form.instance.right_answer == form.instance.user_answer else False
        form.instance.active = True if self.kwargs['answer'] else False

        if not form.instance.user_answer:
            form.instance.sort += 1

        return super().form_valid(form)



