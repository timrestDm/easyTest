from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.base import RedirectView
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
# from mainapp.models import Question

# Create your views here.

class MainView(TemplateView):
	'''Класс отображает главную страницу'''
	template_name = 'mainapp/index.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context


class UsersRedirectView(RedirectView):
	'''Класс для автологина пользователей admin или test при нажатии на соответствующую ссылку'''
	pattern_name = 'mainapp:main'	

	def get_redirect_url(self, *args, **kwargs):
		slug = self.kwargs['slug']
		user = authenticate(username=slug, password=slug)
		login(self.request, user)
		return super().get_redirect_url()


'''
после раскомментирования добавить в файл 'mainapp/urls.py' импорт этого класса и
раскомментировать соответствующую строку в urlpatterns 
'''
# class QuestionListView(ListView):
# 	'''Класс отображает страницу со всеми вопросами'''
# 	model = Question
