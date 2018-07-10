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

from .models import User, FitnessUser, FitnessTrainer, TrainerDoc, TrainerPrice, TrainGym, TrainingSchedule, \
    ProjectionPhoto, MedicalNote, UserDiary, TrainingContract, TrainingPayment, BodyParameter, TargetBodyParameter


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
            if request.POST['password'] == request.POST['password_repeat']:
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

                        messages.add_message(request, messages.SUCCESS,
                                             _("На почту выслана ссылка для активации аккаунта"))

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
class ProfilePage(View):
    """
    Класс отвечает за страницу логина
    """
    content = {}

    def get(self, request):
        if request.user.is_authenticated:
            fitness_user = FitnessUser.objects.get(user = request.user)
            self.content.update({
                'doc': 'pages/personal_area.html',
                'private_doc': 'elements/profile_area.html',
                'fitness_user': fitness_user,
                'user_gyms': TrainGym.objects.filter(user = fitness_user),
                'user_training_schedule': TrainingSchedule.objects.filter(
                                                    Q(target_user = fitness_user) | Q(author_user = fitness_user)).
                                                    filter(schedule_date__gte = now()).order_by('schedule_date')[:6],
                'user_projection_photos': ProjectionPhoto.objects.filter(user = fitness_user).order_by('id')[:6],
                'user_train_contracts': TrainingContract.objects.filter(contract_ward_user = fitness_user,
                                                                        contract_trainer_start = True,
                                                                        contract_trainer_end = False),
                'user_medical_notes': MedicalNote.objects.filter(user = fitness_user).order_by('id')[:6],
                'user_usual_notes': UserDiary.objects.filter(user = fitness_user).order_by('id')[:6]
            })

            # если пользовтель тренер - добавляем данные об аккаунте и документах
            if fitness_user.fitness_user_type == FitnessUser.teacher_user:
                self.content.update({'fitness_trainer': FitnessTrainer.objects.get(user=fitness_user),
                                     'fitness_trainer_docs': TrainerDoc.objects.filter(
                                                                user=FitnessTrainer.objects.get(user = fitness_user)),
                                     'fitness_trainer_price': TrainerPrice.objects.filter(
                                                                user=FitnessTrainer.objects.get(user = fitness_user),
                                                                trainer_price_show = True).order_by('id'),
                                     'fitness_trainer_contracts': TrainingContract.objects.filter(
                                             contract_trainer_user = FitnessTrainer.objects.get(user = fitness_user),
                                             contract_trainer_start = True,
                                             contract_ward_end = False)
                                     })

            return render(request, 'base.html', self.content)
        else:
            return redirect('/private/login/')

    def post(self, request, page):
        return redirect('/private/login/')


# registration
class SuccessLogin(View):
    """
    Класс отвечает за страницу регистрации
    """
    content = {}

    def get(self, request):
        messages.add_message(request, messages.SUCCESS, _('Успешно вошли'))
        return redirect('/private/personal/')

    def post(self, request):
        messages.add_message(request, messages.SUCCESS, _('Успешно вошли'))
        return redirect('/private/personal/')


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


# logout
class LogOutPage(View):
    # get request
    def get(self, request):

        logout(request)

        return redirect('/')


"""
Ajax views
"""


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


"""
Edit view
"""


# edit TrainerPrice
class TrainerPriceEditView(View):
    def post(self, request):
        self.content = {'answer': False}
        # проверка реквеста и авторизироанности пользователя
        if request.is_ajax() and request.user.is_authenticated:
            try:
                # получение данной расценки из БД
                training_price = TrainerPrice.objects.get(id=request.POST['price_id'])
                # проверка пользователя на авторство данной цене
                if training_price.user == FitnessTrainer.objects.get(user__user=request.user):
                    # изменение расценки
                    training_price.trainer_price_hour = request.POST['trainer_price_hour']
                    training_price.trainer_price_comment = request.POST['trainer_price_comment']
                    training_price.trainer_price_currency = request.POST['trainer_price_currency']
                    if 'trainer_price_bargaining' in request.POST:
                        training_price.trainer_price_bargaining = True
                    else:
                        training_price.trainer_price_bargaining = False
                    if 'trainer_price_actuality' in request.POST:
                        training_price.trainer_price_actuality = True
                    else:
                        training_price.trainer_price_actuality = False
                    training_price.save()

                    self.content.update({'answer': True,
                                         'content': _('Данные обновлены')})

            # TODO добавить логгирование ошибок
            except Exception:
                pass

            return JsonResponse(self.content)



























