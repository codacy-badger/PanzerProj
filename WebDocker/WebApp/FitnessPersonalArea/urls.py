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
    # личный кабинет
    path('personal/', views.ProfilePage.as_view(), name='personal_area'),
    path('personal/profile/', views.ProfilePage.as_view(), name='personal_profile'),
    # авторизация через соц-сети
    path('oauth/', include('social_django.urls', namespace='social')),
    # смена языка
    path('change-language/<slug:language>/', views.ChangeLanguage.as_view(), name='language'),
    # выход
    path('logout/', views.LogOutPage.as_view(), name='logout'),

    #Ajax
    # проверка имени пользователя на занятость
    path('username-check/', views.UsernameCheckAjax.as_view(), name='username_check'),
    # проверка имени пользователя на занятость
    path('email-check/', views.EmailCheckAjax.as_view(), name='email_check'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)