from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.utils.translation import activate
from django.utils import translation
from django.utils.translation import ugettext_lazy as _


# смена языка
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
































