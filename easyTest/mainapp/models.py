from django.db import models

# Create your models here.
class Keyword(Core):
    """Тэги""" 
    keyword_name = models.CharField(_('kw-title'), max_length=60,  blank=False)
    def str(self):
        return self.keyword_name

    class Meta:
        verbose_name = _('Тэг')
        verbose_name_plural = _('Тэги)'
        ordering = ('title')


class Question(Core):
    """Вопрос """
    question_text = models.CharField(_('qw_text'), max_length=500, blank=False)
    answers  = models.ForeignKey(Answer, on_delete=models.CASCADE)
    keyword = models.ManyToManyField(Keyword)

    class Meta:
        verbose_name = _('Вопрос')
        verbose_name_plural = _('Вопросы')


