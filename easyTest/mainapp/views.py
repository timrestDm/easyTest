from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView
from django.views.generic.base import RedirectView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from .models import *
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect


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
        return self.model.objects.get_test(self.kwargs['pk'])


class TestList(LoginRequiredMixin, ListView):
    model = Test
    login_url = reverse_lazy('authapp:login')


class ResultCreate(CreateView):
    """docstring for ResultCreate"""
    fields = '__all__'
    model = Result
    slug_url_kwarg = slug_field = 'test'

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.test = form.fields[self.slug_field].to_python(self.kwargs[self.slug_url_kwarg])
        self.success_url = self.request.POST['href']
        return super().form_valid(form)


class ResultDetail(LoginRequiredMixin, DetailView):
    """docstring for ResultDetail"""
    model = Result
    slug_field = 'owner'
    login_url = reverse_lazy('authapp:login')

    def get_object(self):
        self.kwargs[self.slug_url_kwarg] = self.request.user
        try:
            response = super().get_object()
        except:
            response = None
        return response


class ResultUpdate(ResultDetail, UpdateView):
    """docstring for ResultUpdate"""
    fields = '__all__'

    def get_object(self):
        response = super().get_object()
        if not response:
            ResultCreate.as_view()(self.request, *self.args, **self.kwargs)
            response = super().get_object()
        return response

    def form_valid(self, form):
        self.success_url = self.request.POST['href']
        form.instance.owner = self.request.user
        form.instance.test = form.fields['test'].to_python(self.kwargs['test'])

        if self.success_url.endswith('page=2'):          # для обновления результатов при повторном прохождении теста
            form.instance.right_answers_count = 0
            form.instance.wrong_answers_count = 0
            form.instance.time = datetime.now()

        if self.success_url.startswith('/result'):                # Реализация подсчета времени теста
            hours, minutes, seconds = str(form.instance.time).split(':')
            seconds = int(seconds.split('.')[0])
            form.instance.time = datetime.now() - timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))

        if self.request.POST.get('answer') and self.request.POST['answer'] == 'True':
            form.instance.right_answers_count += 1
        else:
            form.instance.wrong_answers_count += 1

        required_correct_answers = Test.objects.get_required_correct_answers(pk=self.kwargs['test'])
        if form.instance.right_answers_count == required_correct_answers:
            form.instance.is_test_passed = True

        response = super().form_valid(form)
        return response


