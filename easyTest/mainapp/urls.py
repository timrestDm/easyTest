from django.urls import path
import mainapp.views as mainapp
from pathlib import PurePath
import os

app_name = PurePath(os.path.dirname(__file__)).parts[-1]

urlpatterns = [
    path('', mainapp.MainView.as_view(), name='main'),
    path('redirect/<slug:slug>/', mainapp.UsersRedirectView.as_view(), name='redirect'),

    path('tests/', mainapp.TestList.as_view(), name='tests'),
    path('test/<int:pk>', mainapp.QuestionList.as_view(), name='test'),
    path('result/<int:test>/', mainapp.ResultDetail.as_view(), name='result'),
    path('result/edit/<int:test>/', mainapp.ResultUpdate.as_view(), name='result_update'),

    # path('questions/', QuestionListView.as_view(), name='questions'),
    ]