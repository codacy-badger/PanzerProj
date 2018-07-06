from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.utils.translation import activate
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse

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
                return redirect('/private/personal/')
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
            # проверяем одинаковость ввелённых паролей
            if request.POST['password']==request.POST['password_repeat']:
                # проверяем отсутствие email среди зарегистрированных
                if not User.objects.filter(email = request.POST['e-mail']):
                    try:
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
                    except:
                        messages.add_message(request, messages.ERROR, _("Ошибка при создании пользователя. "
                                                                        "Ваша почта/логин не уникальны"))
                else:
                    messages.add_message(request, messages.ERROR, _('Email уже используется'))

            else:
                messages.add_message(request, messages.ERROR, _('Введены два разных пароля'))

        return redirect('/private/registration/')


# personal area
class PersonalAreaPage(View):
    """
    Класс отвечает за страницу логина
    """
    content = {}

    def get(self, request):
        self.content.update({
            'doc': 'pages/personal_area.html',
        })
        return render(request, 'base.html', self.content)

    def post(self, request):
        return redirect('/private/login/')


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

# check username in use
class UsernameCheckAjax(View):
    def get(self, request):
        self.content = {'answer': False}
        if request.is_ajax():
            # выбираем переданное имя пользователя
            username = request.GET['username']
            # ищем пользователя с таким же ником в БД
            user = User.objects.filter(username = username)
            if user:
                # если пользователь найден - возвращаем True, иначе False остаётся
                self.content.update({'answer': True})

            return JsonResponse(self.content)


# check email in use
class EmailCheckAjax(View):
    def get(self, request):
        self.content = {'answer': False}
        if request.is_ajax():
            # выбираем переданное email
            email = request.GET['email']
            # ищем пользователя с таким же email в БД
            user = User.objects.filter(email = email)
            if user:
                # если пользователь найден - возвращаем True, иначе False остаётся
                self.content.update({'answer': True})

            return JsonResponse(self.content)




























