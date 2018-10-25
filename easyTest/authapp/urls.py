from django.urls import path, re_path
import authapp.views as authapp
import os
from pathlib import PurePath

app_name = PurePath(os.path.dirname(__file__)).parts[-1]

urlpatterns = [
    path('login/', authapp.Login.as_view(), name='login'),
    path('logout/', authapp.Logout.as_view(), name='logout'),
    path('register/', authapp.CreateProfile.as_view(), name='register'),
    path('edit/', authapp.EditProfile.as_view(), name='edit'),
    path('password/edit', authapp.PasswordChange.as_view(), name='edit_password'),
]



