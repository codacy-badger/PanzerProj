from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # авторизация через соц-сети
    url(r'^oauth/', include('social_django.urls', namespace='social_auth')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)