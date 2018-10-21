from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

# Create your views here.

class MainView(TemplateView):
	'''Класс отображает главную страницу'''
	template_name = 'mainapp/index.html'
