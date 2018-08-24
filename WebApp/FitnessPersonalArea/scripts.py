import json
import timeit
import time

from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.translation import activate
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Q
from django.utils.timezone import now
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.gis.geos import Point
from django.conf import settings


from .models import User, FitnessUser, FitnessTrainer, TrainerDoc, TrainerPrice, TrainGym, TrainingSchedule, \
    ProjectionPhoto, MedicalNote, UserDiary, TrainingContract, TrainingPayment, BodyParameter, BodyParameterData, \
    TargetBodyParameter


# функция отвечает за проверку наличия пользователя в с системе при попытке логина через соц.сеть
def check_social_user_exist(backend, user, response, *args, **kwargs):
    """
    Функция отвечает за проверку наличия данного пользователя в системе.
    Если пользователь новый(не зарегистрирован/не вошёл в аккаунт) - отправляем на регистрацию/вход через логин и пароль
    Если пользователь ранее привязал свой аккаунт в соц.сети к системе - позволяем войти.
    """

    # если пользователь не вошёл в систему зарание - отправляем на регистрацию
    if kwargs['is_new']:
        messages.add_message(kwargs['request'], messages.ERROR, _('Ошибка при входе. Зарегистрируйтесь.'))
        return redirect('registration')
