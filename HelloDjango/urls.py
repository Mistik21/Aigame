from django.contrib import admin
from django.urls import path, include, re_path
from game.views import *
from django.conf import settings
from django.conf.urls.static import static
from core.views import front

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/create-game/', GameAPI.as_view()),
    path("api/game/<int:pk>", GameAPIObject.as_view()),
    path("api/game/", GameListAPI.as_view()),
    path("", front, name="front"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
