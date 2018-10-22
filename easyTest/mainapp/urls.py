from django.urls import path
from mainapp.views import  MainView


app_name = 'mainapp'

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('main/', MainView.as_view(), name='main'),
    # path('questions/', QuestionListView.as_view(), name='questions'),
    ]