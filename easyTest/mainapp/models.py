from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.urls import reverse_lazy


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


class Keyword(Core):
    """Тэги"""
    title = models.CharField(_('Название ключа'), max_length=60, unique=True, blank=False)

    class Meta:
        verbose_name = _('Тэг')
        verbose_name_plural = _('Тэги')


class QuestionManager(CoreManager):
    """docstring for  QuestionManager"""

    pass


class Question(Core):
    """Вопрос """

    # keyword = models.ManyToManyField(Keyword)
    class Meta:
        verbose_name = _('Вопрос')
        verbose_name_plural = _('Вопросы')

    # test = models.ManyToManyField(Test, blank=True, related_name='questions')
    objects = QuestionManager()

    def __str__(self):
        return f'{self.description}'


class AnswerManager(CoreManager):
    """docstring for   AnswerManager"""

    def get_correct_answer(self, question):
        return self.get(question=question, is_correct=True)


class Answer(Core):
    """ класс ответа """

    class Meta:
        verbose_name = _('Ответ')
        verbose_name_plural = _('Ответы')

    # text = models.CharField(_('text'), max_length=250, blank=False)
    is_correct = models.BooleanField(_('is correct'), default=False)
    question = models.ForeignKey(Question, null=True, blank=True, related_name='answers', on_delete=models.CASCADE)
    objects = AnswerManager()

    def __str__(self):
        return f'{self.description}'


class TestCategory(Core):
    """ docstring for TestCategory"""

    cat = models.ForeignKey('self', null=True, blank=True, related_name='test_categories', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Категория теста')
        verbose_name_plural = _('Категории тестов')


class TestManager(CoreManager):
    """docstring for  TestManager"""

    def get_required_correct_answers(self, pk):
        return self.get(pk=pk).required_correct_answers

    def get_questions(self, pk):
        test = self.get(pk=pk)
        return test.questions.all()[:test.max_questions]

    def get_tests(self, request):
        return self.filter(owner=request.user)


class Test(Core):
    """ docstring for Test"""

    class Meta:
        verbose_name = _('Тест')
        verbose_name_plural = _('Тесты')

    owner = models.ForeignKey(User, null=False, blank=True, related_name='tests', on_delete=models.PROTECT)
    category = models.ForeignKey(TestCategory, null=True, blank=True, on_delete=models.SET_NULL)
    keywords = models.ManyToManyField(Keyword, blank=True, related_name='tests')
    questions = models.ManyToManyField(Question, blank=True, related_name='tests')
    max_questions = models.PositiveIntegerField(_('Count questions'), default=0, blank=True)
    required_correct_answers = models.PositiveIntegerField(_('Required correct answers'), default=0, blank=True)
    objects = TestManager()

    TEST_TYPE_CHOICES = (
        ('th', 'teaching'),  # с цифрами (под индексом 0 в кортежах) форма создания теста не проходила, изменил на строку
        ('ex', 'exam'),
        )

    test_type = models.CharField(max_length=2, choices=TEST_TYPE_CHOICES, default='th')
    """ типы тестов - учебный и экзаменационный(на время и оценку) - это реализуем позже.
    Необходимо будет также добавить время на прохождение теста, проценты правильных ответов для разных оценок."""

    def get_absolute_url(self):
        return reverse_lazy('mainapp:tests_staff')


class ResultManager(CoreManager):
    """docstring for  ResultManager"""

    def get_test_queryset(self, request, pk):
        """получаем тест пользователя queryset'ом для ResultCreate (hard_delete) и для ResultDetail"""
        return self.filter(owner=request.user, test_id=pk)

    def get_results(self, request):
        return self.filter(owner=request.user)


class Result(Core):
    """ класс результата """

    class Meta:
        verbose_name = _('Результат')
        verbose_name_plural = _('Результаты')

    owner = models.ForeignKey(User, null=False, blank=True, related_name='results', on_delete=models.PROTECT)
    test = models.ForeignKey(Test, null=True, blank=True, related_name='results', on_delete=models.CASCADE)
    right_answers_count = models.PositiveIntegerField(_('right answers count'), default=0, blank=True)
    wrong_answers_count = models.PositiveIntegerField(_('wrong answers count'), default=0, blank=True)
    time = models.TimeField(_('time for test'), default=timezone.now, blank=True)
    is_test_passed = models.BooleanField(_('is test passed'), default=False)
    objects = ResultManager()

    def __str__(self):
        return f'{self.owner.username}_{self.test.title}'


class UserAnswerManager(CoreManager):
    """docstring for  UserAnswerManager"""

    def get_incorrect_answers(self, request, obj):
        return self.filter(owner=request.user, result=obj, is_correct=False)

    def get_queryset_from_question(self, question):
        return self.filter(question=question)


class UserAnswer(Core):
    """ класс ответа пользователя ответ пользователя создается, только когда он нажимает на кнопку ответить.
    в него записывается ссылка на вопрос, правильный ответ из вопроса и ответ пользователя.
    и это потом аккумулируется в результате теста. т.е.в результ считается только из ответов пользователя.
    при изменении вопроса или теста, ничего пересчитываться не будет """

    class Meta:
        verbose_name = _('Ответ пользователя')
        verbose_name_plural = _('Ответы пользователя')

    owner = models.ForeignKey(User, null=False, blank=True, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, null=False, blank=True, on_delete=models.CASCADE)
    result = models.ForeignKey(Result, null=False, blank=True, related_name='user_answers', on_delete=models.CASCADE)
    right_answer = models.TextField(_('Right answer'), blank=True, null=False)
    user_answer = models.TextField(_('User answer'), blank=True, null=False)
    is_correct = models.BooleanField(_('is user answer correct'), default=False)
    objects = UserAnswerManager()

    def __str__(self):
        return f'{self.owner.username}_{self.result.test.title}__{self.question.description}'
