from django import forms
from django.utils.translation import ugettext_lazy as _
from mainapp.models import Test

class TestForm(forms.ModelForm):
	class Meta:
		model = Test
		fields = ('title', 'description', 'test_type')
		labels = {
			'title': _('Название теста'),
			'description': _('Описание теста'),
			'test_type': _('Тип теста'),
		}