from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView
from authapp.forms import UserLoginForm, UserRegisterForm, UserEditForm
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse_lazy


class Login(SuccessMessageMixin, UserPassesTestMixin, LoginView):
    """docstring for LoginView"""
    template_name = 'authapp/login.html'
    success_message = _('Log in success')
    form_class = UserLoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Log in')
        return context

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return HttpResponseRedirect('/')


class Logout(LogoutView):
    """docstring for logoutView"""
    success_message = _('Log out success')

    def get_next_page(self):
        next_page = super().get_next_page()
        if next_page:
            messages.success(self.request, self.success_message)
        return next_page


class CreateProfile(SuccessMessageMixin, CreateView):
    """docstring for RegisterProfile"""
    template_name = 'authapp/register.html'
    model = User
    form_class = UserRegisterForm
    success_url = '/'
    success_message = _('Registration completed successfully')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Register')
        return context

    def form_valid(self, form):
        form.instance.is_staff = True
        return super().form_valid(form)


class EditProfile(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """docstring for EditProfile"""
    template_name = 'authapp/edit.html'
    login_url = reverse_lazy('authapp:login')
    model = User
    form_class = UserEditForm
    success_url = '/'
    success_message = _('Profile changed')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Edit')
        return context


class DeleteProfile(DeleteView):
    """docstring for DelView"""
    model = User


class PasswordChange(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = 'authapp/password_change_form.html'
    success_message = _('Password changed')
    success_url = reverse_lazy('authapp:edit')

