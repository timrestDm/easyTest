from django.urls import path
import mainapp.views as mainapp
from pathlib import PurePath
import os

app_name = PurePath(os.path.dirname(__file__)).parts[-1]

urlpatterns = [
    path('', mainapp.MainView.as_view(), name='main'),
    path('redirect/<slug:slug>/', mainapp.UsersRedirectView.as_view(), name='redirect'),

    path('test/<int:pk>', mainapp.QuestionList.as_view(), name='test'),
    path('result/<int:pk>', mainapp.ResultDetail.as_view(), name='result'),
    # path('questions/', QuestionListView.as_view(), name='questions'),
    ]