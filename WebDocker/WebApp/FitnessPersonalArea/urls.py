from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from . import views

urlpatterns = [
    # авторизация
    path('login/', views.LoginPage.as_view(), name='login'),
    # успешная авторизация
    path('success/', views.SuccessLogin.as_view(), name='success_login'),
    # регистрация
    path('registration/', views.RegistrationPage.as_view(), name='registration'),
    # авторизация через соц-сети
    path('oauth/', include('social_django.urls', namespace='social')),
    # смена языка
    path('change-language/<slug:language>/', views.ChangeLanguage.as_view(), name='language'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)