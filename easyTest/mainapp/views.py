from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView
# from mainapp.models import Question

# Create your views here.

class MainView(TemplateView):
	'''Класс отображает главную страницу'''
	template_name = 'mainapp/index.html'


'''
после раскомментирования добавить в файл 'mainapp/urls.py' импорт этого класса и
раскомментировать соответствующую строку в urlpatterns 
'''
# class QuestionListView(ListView):
# 	'''Класс отображает страницу со всеми вопросами'''
# 	model = Question
