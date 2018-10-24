from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.views.generic.base import RedirectView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from .models import *


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


class QuestionList(ListView):
    """docstring for test"""
    model = Question
    paginate_by = 1

    def get_queryset(self):
        return self.model.objects.get_test(self.kwargs['pk'])


class ResultCreate(CreateView):
    pass


class ResultDetail(DetailView):
    model = Result

