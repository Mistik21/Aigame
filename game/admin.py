from django.contrib import admin
from .models import Game, Task, FullName, Progress

admin.site.register(Game)
admin.site.register(Task)
admin.site.register(FullName)
admin.site.register(Progress)
