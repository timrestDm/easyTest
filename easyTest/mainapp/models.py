from django.db import models
from django.utils.translation import ugettext_lazy as _

class CoreQuerySet(models.QuerySet):
   """CoreQuerySet need for change initial QuerySet;
    realization soft delete for QuerySet - filter().delete()"""

   def delete(self):
       return super(CoreQuerySet, self).update(deleted=True)

   def hard_delete(self):
       return super(CoreQuerySet, self).delete()


class CoreManager(models.Manager):
   """change initial QuerySet and queryset for superuser in admin_panel"""

   def get_queryset(self):
       return CoreQuerySet(self.model).filter(active=True, deleted=False)

   def get_all_queryset(self):
       return CoreQuerySet(self.model)


class Core(models.Model):
    """docstring for Core; realization soft delete for object - get().delete()"""

    title = models.CharField(_('title'), max_length=250, blank=True)
    description = models.TextField(_('description'), blank=True)
    sort = models.IntegerField(_('sort'), default=0, null=True, blank=True)
    active = models.BooleanField(_('active'), default=True)
    deleted = models.BooleanField(_('deleted'), default=False)

    all_objects = models.Manager()
    objects = CoreManager()

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.title}'

    @property
    def verbose_name(self):
        return self._meta.verbose_name

    @property
    def verbose_name_plural(self):
        return self._meta.verbose_name_plural

    def delete(self):
        self.active = False
        self.save()

    def hard_delete(self):
        self.delete()


# # Create your models here.
# class Keyword(Core):
#     """Тэги""" 
#     title = models.CharField(_('kw-title'), max_length=60, unique = True,  blank=False)
#     def str(self):
#         return self.keyword_name

#     class Meta:
#         verbose_name = _('Тэг')
#         verbose_name_plural = _('Тэги')


class Question(Core):
    """Вопрос """
    # keyword = models.ManyToManyField(Keyword)

    class Meta:
        verbose_name = _('Вопрос')
        verbose_name_plural = _('Вопросы')


class Answer(Core):
    '''класс ответа''' 

    class Meta:
        verbose_name = _('Ответ')
        verbose_name_plural = _('Ответы')

    is_correct = models.BooleanField(_('is correct'), default=False)
    question = models.ForeignKey(Question, null=True, blank=True, related_name='answers', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.description}'


class TestCategory(Core):
    '''docstring for TestCategory'''

    class Meta:
        verbose_name = _('Категория теста')
        verbose_name_plural = _('Категории тестов')



class Test(Core):
    '''docstring for Test'''

    class Meta:
        verbose_name = _('Тест')
        verbose_name_plural = _('Тесты')

    # owner = models.ForeignKey(User, null=False, blank=True, related_name='tests', on_delete=models.PROTECT)
    questions = models.ForeignKey(Question, null=True, blank=True, related_name='tests', on_delete=models.PROTECT)
    # keywords = models.ManyToManyField(Keyword, blank=True)


    category = models.ForeignKey(TestCategory, null=True, blank=True, on_delete=models.SET_NULL)
    max_questions = models.PositiveIntegerField(_('Count questions'), default=0, blank=True)
    required_correct_answers = models.PositiveIntegerField(_('Required correct answers'), default=0, blank=True)


