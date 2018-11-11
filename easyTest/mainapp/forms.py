from django import forms
from django.utils.translation import ugettext_lazy as _
from mainapp.models import Test, TestCategory

class TestForm(forms.ModelForm):
	class Meta:
		model = Test
		fields = ('title', 'description', 'test_type', 'time')
		labels = {
			'title': _('Название теста'),
			'description': _('Описание теста'),
			'test_type': _('Тип теста'),
			'time': _('Время теста'),
		}

class TestCategoryForm(forms.ModelForm):
	class Meta:
		model = TestCategory
		fields = ('title', 'description', 'cat')
		labels = {
			'title': _('Название категории'),
			'description': _('Описание категории'),
			'cat': _('Подкатегория'),
		}