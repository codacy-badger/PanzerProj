import json

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

from geopy.geocoders import Nominatim

from .models import User, FitnessUser, FitnessTrainer, TrainerDoc, TrainerPrice, TrainGym, TrainingSchedule, \
    ProjectionPhoto, MedicalNote, UserDiary, TrainingContract, TrainingPayment, BodyParameter, TargetBodyParameter

from .forms import NewGym


# log in
class LoginPage(View):
    """
    Класс отвечает за страницу логина
    Пользователь ввод логин или e-mail и пароль, затем логинится POST-запросом
    """
    content = {}

    def get(self, request):
        self.content.update({
            'doc': 'pages/login.html',
        })
        return render(request, 'base.html', self.content)

    def post(self, request):
        # получаем из формы поля с логином/e-mail`ом и паролем
        email_username = request.POST['email_username']
        password = request.POST['password']
        try:
            # если передан e-mail
            if '@' in email_username:
                username = User.objects.get(email = email_username).username
            # если передан логин
            else:
                username = email_username
            # пробуем пройти аутентификацию с введёнными данными
            user = authenticate(request, password = password, username = username)
            # при успешной аутентификации
            if user is not None:
                # логиним пользователя
                login(request, user)
                messages.add_message(request, messages.SUCCESS, _('Успешно вошли'))
                # перенаправляем в личный кабинет
                return redirect('personal_profile')
            # при ошибке в введённых данных для входа
            else:
                messages.add_message(request, messages.ERROR, _('Ошибка при входе'))

        except User.DoesNotExist:
            messages.add_message(request, messages.ERROR, _('Такой E-mail не существует'))

        except Exception as err:
            print(err)
            messages.add_message(request, messages.ERROR, _('Ошибка при входе'))

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
    Класс отвечает за личиную страницу
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

                'user_projection_photos': ProjectionPhoto.objects.filter(user = fitness_user).order_by('id')[:4],

                'user_train_contracts': TrainingContract.objects.filter(contract_ward_user = fitness_user,
                                                                        contract_trainer_start = True),

                'user_medical_notes': MedicalNote.objects.filter(user = fitness_user,
                                                                 medical_note_show = True).order_by('-id')[:4],

                'user_usual_notes': UserDiary.objects.filter(user = fitness_user,
                                                             diary_note_show = True).order_by('-id')[:4]
            })

            # если пользовтель тренер - добавляем данные об аккаунте, документах, расценках и
            # контрактах в которых пользователь - тренер
            if fitness_user.fitness_user_type == FitnessUser.teacher_user:
                self.content.update({'fitness_trainer': FitnessTrainer.objects.get(user=fitness_user),
                                     'fitness_trainer_docs': TrainerDoc.objects.filter(
                                                                user__user = fitness_user),
                                     'fitness_trainer_price': TrainerPrice.objects.filter(user__user = fitness_user,
                                                                                          trainer_price_show = True,
                                                                                          trainer_price_actuality = True).
                                                                                    order_by('trainer_price_currency'),
                                     'fitness_trainer_contracts': TrainingContract.objects.filter(
                                             contract_trainer_user = FitnessTrainer.objects.get(user = fitness_user),
                                             contract_trainer_start = True)
                                     })

            return render(request, 'base.html', self.content)
        else:
            return redirect('/private/login/')

    def post(self, request):
        if request.is_ajax() and request.user.is_authenticated:
            ajax_answer = {'answer': False}
            # вносим изменения в описание тренера
            if 'trainer_description' in request.POST:
                try:
                    edited_description = FitnessTrainer.objects.get(user__user = request.user)
                    edited_description.trainer_employment_status = True if 'trainer_employment_status' in request.POST else False
                    edited_description.trainer_description = request.POST['trainer_description']
                    edited_description.save()

                    ajax_answer.update({'answer': True})

                    messages.add_message(request, messages.SUCCESS, _('Данные обновлены'))
                # TODO добавить логгирование ошибок
                except Exception as err:
                    print(err)
                    ajax_answer.update({'error_answer': _('Произошла ошибка!')})

            return JsonResponse(ajax_answer)


# diary notes
class UserDiaryView(View):
    """
    UserDiaryView отвечает за создание, редактирование и просмотр записей в дневник пользователя
    """
    content = {}
    ajax_content = {'answer': False}

    def get(self, request, tag = None):
        if request.user.is_authenticated:
            # если ajax запрос на получение полной информации о записи в дневнике
            if request.is_ajax() and request.GET['diary_note_id']:
                try:
                    diary_note = UserDiary.objects.get(id = request.GET['diary_note_id'])

                    self.ajax_content.update({'answer': True})
                    self.ajax_content['diary_note'] = diary_note.get_note_json()

                # TODO добавить логгирование ошибок
                except Exception as err:
                    print(err)
                    self.ajax_content.update({'error_answer': _('Произошла ошибка!')})

                finally:
                    return JsonResponse(self.ajax_content)

            self.content.update({
                'doc': 'pages/personal_area.html',
                'private_doc': 'pages/diary_notes.html',
                'fitness_user': FitnessUser.objects.get(user = request.user)})

            # ели был передан тег - выбираем записи с ним
            if tag:
                # пагинация по 5 записей c выбранным тегом на страницу и с минимумом на последней - 2
                paginate_view = Paginator(UserDiary.objects.filter(user__user = request.user,
                                                                   diary_note_show = True,
                                                                   diary_note_tags__name__in = [tag]).order_by('-id'),
                                          5, orphans = 2)

            else:
                # пагинация по 5 записей на страницу и с минимумом на последней - 2
                paginate_view = Paginator(UserDiary.objects.filter(user__user = request.user,
                                                                   diary_note_show = True).order_by('-id'),
                                          5, orphans = 2)

            # получаем номер страницы для отображения
            page = request.GET.get('page')
            # получаем набор данных для данной страницы
            self.content.update({'user_usual_notes': paginate_view.get_page(page)})

            return render(request, 'base.html', self.content)

    def post(self, request, tag = None):
        if request.user.is_authenticated:
            # если пользователь хочет удалить пост
            if 'diary_note_delete_id' in request.POST:
                deleted_post = UserDiary.objects.get(id = request.POST['diary_note_delete_id'])
                # проверяем, является ли удаляющий автором поста
                if request.user == deleted_post.user.user:
                    # делаем пост невидимым для пользователя-автора
                    deleted_post.diary_note_show = False
                    deleted_post.save()

                    messages.add_message(request, messages.SUCCESS, _("Запись удалена"))
                else:
                    messages.add_message(request, messages.ERROR, _("Невозможно удалить запись"))

                # возвращаем пользователя назад на ту же страницу
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            """
            Ajax запросы
            """
            # проверка реквеста и авторизироанности пользователя
            if request.is_ajax():
                try:
                    # создаём новую запись в дневнике
                    if 'new_diary_note_btn' in request.POST:
                        try:
                            new_diary_note = UserDiary.objects.create(user = FitnessUser.objects.get(user = request.user),
                                                                      diary_note_title = request.POST['diary_note_title'],
                                                                      diary_note_text = request.POST['diary_note_text'])
                            # добавляем теги к записи в дневнике
                            for tag in request.POST['diary_note_tags'].split(','):
                                new_diary_note.diary_note_tags.add(tag.lower().strip())
                            new_diary_note.save()

                            self.ajax_content.update({'answer': True})

                            messages.add_message(request, messages.SUCCESS, _('Запись создана'))
                        # TODO добавить логгирование ошибок
                        except Exception as err:
                            print(err)
                            self.ajax_content.update({'error_answer': _('Произошла ошибка!')})

                    # редакитурем старую запись в дневнике
                    elif 'diary_note_edit' in request.POST:
                        try:
                            # получаем запись из БД по id
                            diary_note = UserDiary.objects.get(id = request.POST['diary_note_edit'])
                            # проверка соответсвия хозяина заметки и пользователя пытающегося изменить запись
                            if diary_note.user.user == request.user:
                                # вносим изменённые данные в модель записи
                                diary_note.diary_note_title = request.POST['diary_note_title']
                                diary_note.diary_note_text = request.POST['diary_note_text']
                                # обновляем дату записи
                                diary_note.diary_note_datetime = now()

                                # добавляем теги к записи в дневнике
                                for tag in request.POST['diary_note_tags'].split(','):
                                    diary_note.diary_note_tags.add(tag.lower().strip())
                                diary_note.save()

                                self.ajax_content.update({'answer': True})

                                messages.add_message(request, messages.SUCCESS, _('Запись изменена'))
                        # TODO добавить логгирование ошибок
                        except Exception as err:
                            print(err)
                            self.ajax_content.update({'error_answer': _('Произошла ошибка!')})

                # TODO добавить логгирование ошибок
                except Exception as err:
                    print(err)
                    self.ajax_content.update({'error_answer': _('Произошла ошибка!')})

                finally:
                    return JsonResponse(self.ajax_content)


# medical notes
class UserMedicalView(View):
    """
    UserMedicalView отвечает за создание, редактирование и просмотр медицинских записей пользователя
    """
    content = {}
    ajax_content = {'answer': False}

    def get(self, request, tag = None):
        if request.user.is_authenticated:
            # если ajax запрос на получение полной информации о записи в дневнике
            if request.is_ajax() and request.GET['medical_note_id']:
                try:
                    medical_note = MedicalNote.objects.get(id = request.GET['medical_note_id'])

                    self.ajax_content.update({'answer': True})
                    self.ajax_content['medical_note'] = medical_note.get_note_json()

                # TODO добавить логгирование ошибок
                except Exception as err:
                    print(err)
                    self.ajax_content.update({'error_answer': _('Произошла ошибка!')})

                finally:
                    return JsonResponse(self.ajax_content)
            self.content.update({
                'doc': 'pages/personal_area.html',
                'private_doc': 'pages/medical_notes.html',
                'fitness_user': FitnessUser.objects.get(user = request.user)})


            # ели был передан тег - выбираем записи с ним
            if tag:
                # пагинация по 5 записей c выбранным тегом на страницу и с минимумом на последней - 2
                paginate_view = Paginator(MedicalNote.objects.filter(user__user = request.user,
                                                                     medical_note_show = True,
                                                                     medical_note_tags__name__in = [tag]).
                                                                    order_by('-id'),
                                          5, orphans = 2)

            else:
                # пагинация по 5 записей на страницу и с минимумом на последней - 2
                paginate_view = Paginator(MedicalNote.objects.filter(user__user = request.user,
                                                                     medical_note_show = True).order_by('-id'),
                                          5, orphans = 2)

            # получаем номер страницы для отображения
            page = request.GET.get('page')
            # получаем набор данных для данной страницы
            self.content.update({'user_medical_notes': paginate_view.get_page(page)})

            return render(request, 'base.html', self.content)

    def post(self, request, tag = None):
        if request.user.is_authenticated:
            # если пользователь хочет удалить пост
            if 'medical_note_delete_id' in request.POST:
                deleted_post = MedicalNote.objects.get(id = request.POST['medical_note_delete_id'])
                # проверяем, является ли удаляющий автором поста
                if request.user == deleted_post.user.user:
                    # делаем пост невидимым для пользователя-автора
                    deleted_post.medical_note_show = False
                    deleted_post.save()

                    messages.add_message(request, messages.SUCCESS, _("Запись удалена"))
                else:
                    messages.add_message(request, messages.ERROR, _("Невозможно удалить запись"))

                # возвращаем пользователя назад на ту же страницу
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            """
            Ajax запросы
            """
            # проверка реквеста и авторизироанности пользователя
            if request.is_ajax():
                try:
                    # создаём новую медицинскую запись запись в дневнике
                    if 'new_medical_note_btn' in request.POST:
                        try:
                            new_medical_note = MedicalNote.objects.create(
                                user = FitnessUser.objects.get(user = request.user),
                                medical_note_title = request.POST['medical_note_title'],
                                medical_note_text = request.POST['medical_note_text'])

                            # добавляем теги к медицинской записи
                            for tag in request.POST['medical_note_tags'].split(','):
                                new_medical_note.medical_note_tags.add(tag.lower().strip())
                            new_medical_note.save()

                            self.ajax_content.update({'answer': True})

                            messages.add_message(request, messages.SUCCESS, _('Запись создана'))
                        # TODO добавить логгирование ошибок
                        except Exception as err:
                            print(err)
                            self.ajax_content.update({'error_answer': _('Произошла ошибка!')})

                    # редакитурем старую мед. запись
                    elif 'medical_note_edit' in request.POST:
                        try:
                            # получаем запись из БД по id
                            medical_note = MedicalNote.objects.get(id = request.POST['medical_note_edit'])
                            # проверка соответсвия хозяина мед.заметки и пользователя пытающегося изменить запись
                            if medical_note.user.user == request.user:
                                # вносим изменённые данные в модель записи
                                medical_note.medical_note_title = request.POST['medical_note_title']
                                medical_note.medical_note_text = request.POST['medical_note_text']
                                # обновляем дату записи
                                medical_note.medical_note_datetime = now()

                                # добавляем теги к записи в дневнике
                                for tag in request.POST['medical_note_tags'].split(','):
                                    medical_note.medical_note_tags.add(tag.lower().strip())
                                medical_note.save()

                                self.ajax_content.update({'answer': True})

                                messages.add_message(request, messages.SUCCESS, _('Запись изменена'))
                        # TODO добавить логгирование ошибок
                        except Exception as err:
                            print(err)
                            self.ajax_content.update({'error_answer': _('Произошла ошибка!')})
                # TODO добавить логгирование ошибок
                except Exception as err:
                    self.ajax_content.update({'error_answer': _('Произошла ошибка!')})

        return JsonResponse(self.ajax_content)


# user gym`s
class UserGymsView(View):
    """
    UserGymsView отвечает за страницу с тренажёрными залами пользователя,
        а так же создание, редактирование и просмотр всех залов
    """
    content = {}

    def get(self, request):
        if request.user.is_authenticated:
            # получаем данные пользователя
            fitness_user = FitnessUser.objects.get(user = request.user)
            # проверяем тип пользователя, должен быть тренером
            if fitness_user.fitness_user_type == FitnessUser.teacher_user:
                self.content.update({
                    'doc': 'pages/personal_area.html',
                    'private_doc': 'pages/gyms.html',
                    'fitness_user': fitness_user,
                    'fitness_user_gyms': TrainGym.objects.filter(user = fitness_user).order_by('id'),
                    'fitness_user_gyms_json': serialize('geojson', TrainGym.objects.filter(user = fitness_user),
                                                  geometry_field='gym_geo',
                                                  fields=('gym_geo','gym_destination', 'gym_description','gym_name'))})

                return render(request, 'base.html', self.content)

    def post(self, request):
        self.ajax_content = {'answer': False}
        # проверка аторизованности пользователя
        if request.user.is_authenticated:
            fitness_user = FitnessUser.objects.get(user = request.user)
            # если отправлен AJAX запрос
            if request.is_ajax():
                print(request.POST)
                try:
                    if request.POST.get('new_gym_btn_id'):
                        gym_position = Nominatim().geocode(request.POST['gym_adress'])
                        if gym_position:
                            # создаём новый зал
                            TrainGym.objects.create(user = fitness_user,
                                                    gym_name = request.POST['gym_title'],
                                                    gym_description = request.POST['gym_description'],
                                                    gym_destination = request.POST['gym_adress'],
                                                    # получаем точку размещения данного адреса
                                                    gym_geo = Point(gym_position.longitude, gym_position.latitude,
                                                                    srid = gym_position.raw['place_id']))

                            messages.add_message(request, messages.SUCCESS, _('Зал сохранён'))
                            # обновляем ответ на AJAX-запрос, об успешном создании зала
                            self.ajax_content.update({'answer': True})
                        else:
                            # обновляем ответ на AJAX-запрос, об ошибке при декодировании адреса в местоположение
                            self.ajax_content.update({'error_answer': _('Данный адрес не найден')})
                        '''
                        # локацию (долготу/широту) в адрес
                        new_gym_destination = Nominatim().reverse(new_gym_form.cleaned_data['gym_destination'])
                        new_gym.gym_destination = new_gym_destination
                        new_gym.save()
                        '''
                    elif request.POST.get('gym_edit'):
                        print('Edit old GYM')

                # TODO добавить логгирование ошибок
                except Exception as err:
                    print(err)
                    self.ajax_content.update({'error_answer': _('Произошла ошибка!')})

                finally:
                    return JsonResponse(self.ajax_content)


# trainer price page
class TrainerPriceView(View):
    """
    TrainerPriceView отвечает за страницу с расценками тренера,
        а так же создание, редактирование и просмотр расценок тренера
    """
    content = {}

    def get(self, request):
        if request.user.is_authenticated:
            self.content.update({
                'doc': 'pages/personal_area.html',
                'private_doc': 'pages/trainer_prices.html',
                'fitness_user': FitnessUser.objects.get(user = request.user),
                'fitness_trainer_price': TrainerPrice.objects.filter(user__user__user = request.user,
                                                                     trainer_price_show = True).
                                order_by('id')})

            return render(request, 'base.html', self.content)

    def post(self, request):
        self.ajax_content = {'answer': False}
        # проверка реквеста и авторизироанности пользователя
        if request.is_ajax() and request.user.is_authenticated:
            try:
                # если id расценки -0, создаём новую
                if request.POST['price_id'] == '0':
                    # создаём новую расценку
                    TrainerPrice.objects.create(user = FitnessTrainer.objects.get(user__user = request.user),
                                                trainer_price_hour = request.POST['trainer_price_hour'],
                                                trainer_price_comment = request.POST['trainer_price_comment'],
                                                trainer_price_currency = request.POST['trainer_price_currency'],
                                                trainer_price_bargaining = True if 'trainer_price_bargaining' in request.POST else False,
                                                trainer_price_actuality = True if 'trainer_price_actuality' in request.POST else False)

                    # обновляем данные для ответа сервера
                    self.ajax_content.update({'answer': True})
                    # добавляем сообщение пользователю
                    messages.add_message(request, messages.SUCCESS, _('Расценка создана'))

                else:
                    # если изменяем расценку - получение данной расценки из БД
                    training_price = TrainerPrice.objects.get(id=request.POST['price_id'])
                    # проверка пользователя на авторство данной цене
                    if training_price.user == FitnessTrainer.objects.get(user__user=request.user):
                        # изменение расценки
                        training_price.trainer_price_hour = request.POST['trainer_price_hour']
                        training_price.trainer_price_comment = request.POST['trainer_price_comment']
                        training_price.trainer_price_currency = request.POST['trainer_price_currency']

                        training_price.trainer_price_bargaining = True if 'trainer_price_bargaining' in request.POST else False

                        training_price.trainer_price_actuality = True if 'trainer_price_actuality' in request.POST else False

                        # сохраняем новые данные расценки
                        training_price.save()

                        # обновляем данные для ответа сервера
                        self.ajax_content.update({'answer': True})
                        # добавляем сообщение пользователю
                        messages.add_message(request, messages.SUCCESS, _('Данные обновлены'))

            # TODO добавить логгирование ошибок
            except Exception as err:
                self.ajax_content.update({'error_answer': _('Произошла ошибка!')})

            finally:
                return JsonResponse(self.ajax_content)


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
    """
    Класс отвечает за выход из сервиса
    """
    # get request
    def get(self, request):

        logout(request)

        return redirect('/')


# success login
class SuccessLogin(View):
    """	
    SuccessLogin отвечает за redirect после логина через соц.сети	
    """
    content = {}

    def get(self, request):
        messages.add_message(request, messages.SUCCESS, _('Успешно вошли'))
        return redirect('/private/personal/')

    def post(self, request):
        messages.add_message(request, messages.SUCCESS, _('Успешно вошли'))
        return redirect('/private/personal/')


"""
Ajax views
"""


# check username in use
class UsernameCheckAjax(View):
    """
    Класс отвечает за проверку наличия имени пользователя в сервисе
    Пользователь присылает GET-Ajax запрос и получает форматированный JSON-ответ.
    {'answer': False(пользователя с таким ником нет)/True(пользователь с таким нимком есть)}
    """
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
    """
    Класс отвечает за проверку наличия e-mail`а в сервисе
    Пользователь присылает GET-Ajax запрос и получает форматированный JSON-ответ.
    {'answer': False(e-mail`а в сервисе нет)/True(e-mail в сервисе есть)}
    """
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
