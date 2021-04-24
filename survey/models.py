from django.db import models


class Survey(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название')
    start_date = models.DateField(auto_now=True, verbose_name='Дата старта')
    end_date = models.DateField(auto_now_add=True, verbose_name='Дата окончания')
    description = models.TextField(blank=True, verbose_name='Описание')
    visible = models.BooleanField(default=False, verbose_name='Включен')
