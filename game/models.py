from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    task_count = models.CharField(max_length=100)
    topic = models.CharField(max_length=500)
    link = models.TextField(blank=True)


class Game(models.Model):
    title = models.CharField(max_length=150)
    class_user = models.CharField(max_length=2)
    count_checkpoint = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    img = models.ImageField(upload_to='images')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    users = models.TextField(blank=True)
    checkpoint = models.ManyToManyField(Task)


class FullName(models.Model):
    name = models.CharField(verbose_name='Имя', max_length=40)
    surname = models.CharField(verbose_name='Фамилия', max_length=40)
    middle_name = models.CharField(verbose_name='Отчество', max_length=40)
    user = models.OneToOneField(User, on_delete=models.CASCADE)