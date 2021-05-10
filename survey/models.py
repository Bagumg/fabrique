from datetime import date

from django.db import models


class Users(models.Model):
    """
    Модель пользователя
    """

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return str(self.id)


class Survey(models.Model):
    """
    Модель опроса
    """
    name = models.CharField(max_length=64, verbose_name='Название')
    start_date = models.DateField(auto_created=True, default=date.today, verbose_name='Дата старта', editable=True)
    end_date = models.DateField(verbose_name='Дата окончания')
    description = models.TextField(blank=True, verbose_name='Описание')
    visible = models.BooleanField(default=False, verbose_name='Включен')

    class Meta:
        verbose_name = 'опрос'
        verbose_name_plural = 'опросы'

    def __str__(self):
        return self.name


class Question(models.Model):
    """
    Модель вопроса
    """
    CHOICES = [
        ('TEXT', 'Ответ текстом'),
        ('SELECT', 'Ответ с выбором одного варианта'),
        ('SELECT_MULTIPLE', 'Ответ с выбором нескольких вариантов'),
    ]
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name='Опрос')
    text = models.TextField(verbose_name='Текст вопроса')
    question_type = models.CharField(choices=CHOICES, max_length=128, verbose_name='Тип вопроса')

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'

    def __str__(self):
        return self.text


class Answer(models.Model):
    """
    Модель ответа
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    data = models.TextField(verbose_name='Данные ответа')
    user_id = models.ForeignKey(Users, default=1, on_delete=models.CASCADE, verbose_name='ID пользователя', blank=False)

    class Meta:
        verbose_name = 'ответ'
        verbose_name_plural = 'ответы'

    def __str__(self):
        return f'Ответ на вопрос: {self.question}'
