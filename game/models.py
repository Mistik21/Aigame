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


class Progress(models.Model):
    progress_user = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


class FullName(models.Model):
    FIO_user = models.CharField(verbose_name='Имя', max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='fio')
    progress_game = models.ManyToManyField(Progress)
#     def get_full_info(self):
#         return self


# class UserFullInfoMixin:
#     def get_full_info(self):
#         try:
#             return self
#         except:
#             return None

# User.__bases__ = (UserFullInfoMixin,) + User.__bases__