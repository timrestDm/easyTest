from django.urls import path
from mainapp.views import  MainView, UsersRedirectView


app_name = 'mainapp'

urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('main/', MainView.as_view(), name='main'),
    path('redirect/<slug:slug>/', UsersRedirectView.as_view(), name='redirect'),
    # path('questions/', QuestionListView.as_view(), name='questions'),
    ]