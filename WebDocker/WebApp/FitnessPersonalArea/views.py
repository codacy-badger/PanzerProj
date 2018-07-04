from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.utils.translation import activate
from django.utils import translation
from django.utils.translation import ugettext_lazy as _


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
        pass


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
        pass


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
































