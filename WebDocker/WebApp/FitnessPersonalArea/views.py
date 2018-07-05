from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.utils.translation import activate
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate, login
from django.contrib import messages

from .models import User, FitnessUser


# log in
class LoginPage(View):
    """
    Класс отвечает за страницу логина
    """
    content = {}

    def get(self, request):
        self.content.update({
            'doc': 'pages/login.html',
        })
        return render(request, 'base.html', self.content)

    def post(self, request):
        email_username = request.POST['email_username']
        password = request.POST['password']
        try:
            if '@' in email_username:
                username = User.objects.get(email = email_username).username
            else:
                username = email_username
            user = authenticate(request, password = password, username = username)
            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, _('Успешно вошли'))
                return redirect('/private/login/')
            else:
                messages.add_message(request, messages.ERROR, _('Ошибка при входе'))
        except:
            messages.add_message(request, messages.ERROR, _('Такой E-mail не существует'))

        return redirect('/private/login/')


# registration
class RegistrationPage(View):
    """
    Класс отвечает за страницу регистрации
    """
    content = {}

    def get(self, request):
        self.content.update({
            'doc': 'pages/registration.html',
        })
        return render(request, 'base.html', self.content)

    def post(self, request):
        if 'new_account_btn' in request.POST:
            if request.POST['password']==request.POST['password']:
                # создаём нового пользователя
                new_user = User.objects.create_user(username = request.POST['username'],
                                                    email = request.POST['e-mail'],
                                                    password = request.POST['password'],
                                                    first_name = request.POST['name'],
                                                    last_name = request.POST['surname'])
                new_user.is_active = False
                new_user.save()
                # создаём нового пользователя с дополнительными полями
                FitnessUser.objects.create(user = new_user,
                                           fitness_user_type = request.POST['account_type'],
                                           fitness_user_gender = request.POST['gender'])

                messages.add_message(request, messages.SUCCESS, _("На почту выслана ссылка для активации аккаунта"))

                return redirect('/private/login/')
            else:
                messages.add_message(request, messages.ERROR, _('Введены два разных пароля'))

        return redirect('/private/registration/')


# registration
class SuccessLogin(View):
    """
    Класс отвечает за страницу регистрации
    """
    content = {}

    def get(self, request):
        print(request)
        print(request.GET)
        messages.add_message(request, messages.SUCCESS, _('Успешно вошли'))
        return redirect('/private/login/')

    def post(self, request):
        print(request)
        print(request.POST)
        messages.add_message(request, messages.SUCCESS, _('Успешно вошли'))
        return redirect('/private/login/')


# change language
class ChangeLanguage(View):
    """
    Класс отвечает за смену языка интерфейса
    """
    def get(self, request, language):
        """
        Метод отвечает за принятие GET запроса с новым языком интерфейса
        :param request:
        :param language: Выбранный язык
        :return: Перенаправляет на главную страницу и задаёт новый язык
        """

        translation.activate(language)
        request.session[translation.LANGUAGE_SESSION_KEY] = language

        return redirect('home')
































