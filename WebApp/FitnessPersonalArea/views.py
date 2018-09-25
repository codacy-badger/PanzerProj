import logme

from django.shortcuts import render
from django.views import View
from django.shortcuts import redirect
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.utils.timezone import now
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.contrib.gis.geos import Point
from django.conf import settings


from geopy.geocoders import GoogleV3

from .models import User, FitnessUser, FitnessTrainer, TrainerDoc, TrainerPrice, TrainGym, TrainingSchedule, \
    ProjectionPhoto, MedicalNote, UserDiary, TrainingContract, TrainingPayment, BodyParameter, BodyParameterData, \
    TargetBodyParameter

from .forms import NewParameterData


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
                messages.add_message(request, messages.ERROR, _('Ошибка при входе. Проверьте введённые данные'))

        except User.DoesNotExist:
            messages.add_message(request, messages.ERROR, _('Такой E-mail не существует'))

        except Exception as err:
            print(err)
            messages.add_message(request, messages.ERROR, _('Ошибка при входе, Обратитесь к администрации'))

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
        if request.POST.get('new_account_btn'):
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
@logme.log
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
                'user_gyms': TrainGym.objects.filter(user = fitness_user).order_by('-id')[:4],

                'user_training_schedule': TrainingSchedule.objects.filter(
                                                    Q(target_user = fitness_user) | Q(author_user = fitness_user)).
                                                    filter(schedule_date__gte = now()).order_by('schedule_date')[:6],

                'user_projection_photos': ProjectionPhoto.objects.filter(user = fitness_user).order_by('id')[:4],

                'user_train_contracts': TrainingContract.objects.filter(contract_ward_user = fitness_user,
                                                                        contract_trainer_start = True),

                'user_medical_notes': MedicalNote.objects.filter(user = fitness_user,
                                                                 medical_note_show = True).order_by('-id')[:4],
                # получаем записи из дневника пользователя
                'user_usual_notes': UserDiary.objects.filter(user = fitness_user,
                                                             diary_note_show = True).order_by('-id')[:4],
                # получаем залы пользователя
                'fitness_user_gyms_json': serialize('geojson', TrainGym.objects.filter(user = fitness_user),
                                                    geometry_field = 'gym_geo',
                                                    fields = ('gym_geo',
                                                              'gym_destination',
                                                              'gym_description',
                                                              'gym_name')
                                                    ),
                # получаем праметры пользователя
                'user_body_params': BodyParameterData.objects.filter(user_parameter__user = fitness_user,
                                                                     user_parameter__body_show = True).
                                                order_by('user_parameter', '-body_datetime').distinct('user_parameter')[:4]
            })

            # если пользовтель тренер - добавляем данные об аккаунте, документах, расценках и
            # контрактах в которых пользователь - тренер
            if fitness_user.fitness_user_type == FitnessUser.teacher_user:
                self.content.update({'fitness_trainer': FitnessTrainer.objects.get(user=fitness_user),
                                     'fitness_trainer_docs': TrainerDoc.objects.filter(
                                                                user__user = fitness_user)[:4],
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
            messages.add_message(request, messages.ERROR, _('Нехватает прав для просмотра'))
            # возвращаем пользователя назад на ту же страницу
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def post(self, request):
        if request.is_ajax() and request.user.is_authenticated:
            ajax_answer = {'answer': False}
            try:
                # вносим изменения в описание тренера
                if request.POST.get('trainer_description'):
                    edited_description = FitnessTrainer.objects.get(user__user = request.user)
                    edited_description.trainer_employment_status = True if request.POST.get('trainer_employment_status') else False
                    edited_description.trainer_description = request.POST['trainer_description']
                    edited_description.save()

                    ajax_answer.update({'answer': True})

                    messages.add_message(request, messages.SUCCESS, _('Данные обновлены'))
            except Exception as err:
                self.logger.error(f'In - ProfilePage.post; '
                                  f'User - {request.user}; '
                                  f'Sended params - {request.POST.get("trainer_description")}; '
                                  f'Text - {err} ')
                ajax_answer.update({'error_answer': _('Произошла ошибка!')})
            finally:
                return JsonResponse(ajax_answer)


# diary notes
@logme.log
class UserDiaryView(View):
    """
    UserDiaryView отвечает за создание, редактирование и просмотр записей в дневник пользователя
    """
    content = {}
    ajax_content = {'answer': False}

    def get(self, request, tag: str = None):
        if request.user.is_authenticated:
            # если ajax запрос на получение полной информации о записи в дневнике
            if request.is_ajax() and request.GET.get('diary_note_id'):
                try:
                    diary_note = UserDiary.objects.get(id = request.GET['diary_note_id'],
                                                       user__user = request.user,
                                                       diary_note_show = True)

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

    def post(self, request, tag: str = None):
        if request.user.is_authenticated:
            fitness_user = FitnessUser.objects.get(user = request.user)
            # если пользователь хочет удалить пост
            if request.POST.get('diary_note_delete_id'):
                try:
                    deleted_post = UserDiary.objects.get(id = request.POST['diary_note_delete_id'])
                    # проверяем, является ли удаляющий автором поста
                    if fitness_user == deleted_post.user:
                        # делаем пост невидимым для пользователя-автора
                        deleted_post.diary_note_show = False
                        deleted_post.save()

                        messages.add_message(request, messages.SUCCESS, _("Запись удалена"))
                    else:
                        messages.add_message(request, messages.ERROR, _("Невозможно удалить запись"))

                # TODO добавить логгирование ошибок
                except Exception as err:
                    self.logger.error(f'In - UserDiaryView.post; '
                                      f'User - {request.user}; '
                                      f'Sended params - {request.POST.get("diary_note_delete_id")}; '
                                      f'Text - {err} ')
                    messages.add_message(request, messages.ERROR, _("Невозможно удалить запись. Ошибка."))
                finally:
                    # возвращаем пользователя назад на ту же страницу
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            """
            Ajax запросы
            """
            # проверка реквеста и авторизироанности пользователя
            if request.is_ajax():
                try:
                    # создаём новую запись в дневнике
                    if request.POST.get('new_diary_note_btn'):
                        new_diary_note = UserDiary.objects.create(user = FitnessUser.objects.get(user = request.user),
                                                                  diary_note_title = request.POST['diary_note_title'],
                                                                  diary_note_text = request.POST['diary_note_text'])
                        # добавляем теги к записи в дневнике
                        for tag in request.POST['diary_note_tags'].split(','):
                            new_diary_note.diary_note_tags.add(tag.lower().strip())
                        new_diary_note.save()

                        self.ajax_content.update({'answer': True})

                        messages.add_message(request, messages.SUCCESS, _('Запись создана'))

                    # редакитурем старую запись в дневнике
                    elif request.POST.get('diary_note_edit'):
                        # получаем запись из БД по id
                        diary_note = UserDiary.objects.get(id = request.POST['diary_note_edit'])
                        # проверка соответсвия хозяина заметки и пользователя пытающегося изменить запись
                        if diary_note.user == fitness_user:
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

                finally:
                    return JsonResponse(self.ajax_content)


# medical notes
class UserMedicalView(View):
    """
    UserMedicalView отвечает за создание, редактирование и просмотр медицинских записей пользователя
    """
    content = {}
    ajax_content = {'answer': False}

    def get(self, request, tag: str = None):
        if request.user.is_authenticated:
            # если ajax запрос на получение полной информации о записи в дневнике
            if request.is_ajax() and request.GET['medical_note_id']:
                try:
                    medical_note = MedicalNote.objects.get(id = request.GET['medical_note_id'], user__user = request.user)

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

        else:
            messages.add_message(request, messages.ERROR, _('Недостаточно прав'))
            # возвращаем пользователя назад на ту же страницу
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def post(self, request, tag: str = None):
        if request.user.is_authenticated:
            fitness_user = FitnessUser.objects.get(user = request.user)
            # если пользователь хочет удалить пост
            if request.POST.get('medical_note_delete_id'):
                try:
                    deleted_post = MedicalNote.objects.get(id = request.POST['medical_note_delete_id'])
                    # проверяем, является ли удаляющий автором поста
                    if fitness_user == deleted_post.user:
                        # делаем пост невидимым для пользователя-автора
                        deleted_post.medical_note_show = False
                        deleted_post.save()

                        messages.add_message(request, messages.SUCCESS, _("Запись удалена"))
                    else:
                        messages.add_message(request, messages.ERROR, _("Невозможно удалить запись"))

                # TODO добавить логгирование ошибок
                except Exception as err:
                    print(err)
                    messages.add_message(request, messages.ERROR, _("Невозможно удалить запись. Ошибка."))
                finally:
                    # возвращаем пользователя назад на ту же страницу
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            """
            Ajax запросы
            """
            # проверка реквеста и авторизироанности пользователя
            if request.is_ajax():
                try:
                    # создаём новую медицинскую запись запись в дневнике
                    if request.POST.get('new_medical_note_btn'):
                        new_medical_note = MedicalNote.objects.create(
                            user = fitness_user,
                            medical_note_title = request.POST['medical_note_title'],
                            medical_note_text = request.POST['medical_note_text'])

                        # добавляем теги к медицинской записи
                        for tag in request.POST['medical_note_tags'].split(','):
                            new_medical_note.medical_note_tags.add(tag.lower().strip())
                        new_medical_note.save()

                        self.ajax_content.update({'answer': True})

                        messages.add_message(request, messages.SUCCESS, _('Запись создана'))

                    # редакитурем старую мед. запись
                    elif request.POST.get('medical_note_edit'):
                        # получаем запись из БД по id
                        medical_note = MedicalNote.objects.get(id = request.POST['medical_note_edit'])
                        # проверка соответсвия хозяина мед.заметки и пользователя пытающегося изменить запись
                        if medical_note.user == fitness_user:
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
                    self.ajax_content.update({'error_answer': _('Произошла ошибка!')})

                finally:
                    return JsonResponse(self.ajax_content)


# user gym`s
class UserGymsView(View):
    """
    UserGymsView отвечает за страницу с тренажёрными залами пользователя,
        а так же создание, редактирование и просмотр всех залов
    """
    content = {}
    ajax_content = {'answer': False}

    def get(self, request):
        if request.user.is_authenticated:
            # получаем данные пользователя
            fitness_user = FitnessUser.objects.get(user = request.user)
            if request.is_ajax() and request.GET.get('gym_object_id'):

                try:
                    # получаем данные зала из БД
                    gym_object = TrainGym.objects.get(id = request.GET['gym_object_id'], user = fitness_user)
                    self.ajax_content.update({'gym_data': gym_object.get_gym_json()})

                # TODO добавить логгирование ошибок
                except Exception as err:
                    print(err)
                    self.ajax_content.update({'error_answer': _('Произошла ошибка!')})

                finally:
                    return JsonResponse(self.ajax_content)
            else:

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
        # проверка аторизованности пользователя
        if request.user.is_authenticated:
            fitness_user = FitnessUser.objects.get(user = request.user)
            # если отправлен AJAX запрос
            if request.is_ajax():
                try:
                    # при создании нового зала
                    if request.POST.get('new_gym_btn_id'):
                        gym_position = GoogleV3(api_key = settings.GGLE_MAP_API_KEY).geocode(request.POST['gym_adress'])
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
                    # при редактировании имебщегося зала
                    elif request.POST.get('gym_edit'):
                        # декодируем адрес в положение на карте
                        gym_position = GoogleV3(api_key = settings.GGLE_MAP_API_KEY).geocode(request.POST['gym_adress'])
                        if gym_position:
                            # получаем зал по ID
                            edited_gym = TrainGym.objects.get(id = request.POST['gym_edit'])
                            # проверяем, является ли пользователь владельцем записи о зале
                            if fitness_user == edited_gym.user:
                                # обновляем данные зала
                                edited_gym.gym_name = request.POST['gym_title']
                                edited_gym.gym_description = request.POST['gym_description']
                                edited_gym.gym_destination = request.POST['gym_adress']
                                edited_gym.gym_geo = Point(gym_position.longitude, gym_position.latitude,
                                                           srid = gym_position.raw['place_id'])

                                edited_gym.save()

                                messages.add_message(request, messages.SUCCESS, _('Изменения сохранены'))
                                # обновляем ответ на AJAX-запрос, об успешном создании зала
                                self.ajax_content.update({'answer': True})
                            else:
                                # обновляем ответ на AJAX-запрос, с проблемой на права доступа
                                self.ajax_content.update({'answer': False,
                                                          'error_answer': _('Нехвататет прав для действия')})
                        else:
                            # обновляем ответ на AJAX-запрос, об ошибке при декодировании адреса в местоположение
                            self.ajax_content.update({'error_answer': _('Данный адрес не найден')})

                # TODO добавить логгирование ошибок
                except Exception as err:
                    print(err)
                    self.ajax_content.update({'error_answer': _('Произошла ошибка!')})

                finally:
                    return JsonResponse(self.ajax_content)
            else:
                # при удалении отслеживаемого параметра
                if request.POST.get('gym_id'):
                    # получаем данные зала
                    delete_gym = TrainGym.objects.get(id = request.POST['gym_id'])
                    # проверка прав доступа
                    if delete_gym.user == fitness_user:
                        # меняем область видимости на False и сохраняем модель
                        delete_gym.delete()

                        messages.add_message(request, messages.SUCCESS, _('Данные удалены'))
                    else:
                        messages.add_message(request, messages.ERROR, _('Данные не удалены. Недостаточно прав.'))

                # возвращаем пользователя назад на ту же страницу
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# user params
class UserParamsView(View):
    """
    UserParamsView отвечает за страницу с отслеживаемыми параметрами пользователя
    """
    content = {}
    ajax_content = {'answer': False}

    def get(self, request):
        if request.user.is_authenticated:
            # получаем данные пользователя
            fitness_user = FitnessUser.objects.get(user = request.user)
            # если получен AJAX-get запрос с ID параметра
            if request.is_ajax() and request.GET.get('param_object_id'):

                try:
                    # получаем данные параметра из БД. Нулевой элемент
                    param_data = BodyParameterData.objects.filter(user_parameter__id = request.GET['param_object_id'],
                                                                  user_parameter__body_show = True).first()

                    # проверка прав на получение информации о параметре
                    if param_data.user_parameter.user == fitness_user:
                        self.ajax_content.update({'param_json_data': param_data.get_param_json()})
                    else:
                        self.ajax_content.update({'error_answer': _('Недостаточно прав')})

                # TODO добавить логгирование ошибок
                except Exception as err:
                    print(err)
                    self.ajax_content.update({'error_answer': _('Произошла ошибка!')})

                finally:
                    return JsonResponse(self.ajax_content)
            else:
                # получаем номер страницы для отображения при пагинации
                page = request.GET.get('page')

                self.content.update({
                    'doc': 'pages/personal_area.html',
                    'private_doc': 'pages/user_params.html',
                    'fitness_user': fitness_user,
                    'new_param_data_form': NewParameterData({'user_id': request.user.id}),

                    'user_body_params': Paginator(BodyParameterData.objects.filter(user_parameter__user = fitness_user,
                                                                                   user_parameter__body_show = True).
                        order_by('user_parameter', '-body_datetime').distinct('user_parameter'), 5, orphans = 2).get_page(page)
                })

                return render(request, 'base.html', self.content)
        else:

            messages.add_message(request, messages.ERROR, _('Недостаточно прав для просмотра'))
            # возвращаем пользователя назад на ту же страницу
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def post(self, request):
        # проверка аторизованности пользователя
        if request.user.is_authenticated:
            fitness_user = FitnessUser.objects.get(user = request.user)
            # если отправлен AJAX запрос
            if request.is_ajax():
                try:
                    # при создании нового параметра для слежения
                    if request.POST.get('new_body_parameter_id'):
                        # создаём новый параметр для отслеживания
                        new_param = BodyParameter.objects.create(user = fitness_user,
                                                                 body_title = request.POST['body_title'])

                        # вводим первоначальные значения параметра
                        BodyParameterData.objects.create(user_parameter = new_param,
                                                         body_data = request.POST['body_data'])

                        # вводим первоначальную цель для отслеживания
                        TargetBodyParameter.objects.create(target_parameter = new_param,
                                                           target_body_data = request.POST['target_body_data'])

                        messages.add_message(request, messages.SUCCESS, _('Параметр сохранён'))
                        # обновляем ответ на AJAX-запрос, об успешном создании зала
                        self.ajax_content.update({'answer': True})

                    # при добавлении новый данных от пользователя
                    elif request.POST.get('new_body_param_data_id'):
                        # получаем параметр для отслеживания
                        add_data_param = BodyParameter.objects.get(id = request.POST['param_id'])

                        # вводим новое значения параметра
                        BodyParameterData.objects.create(user_parameter = add_data_param,
                                                         body_data = request.POST['body_param_data'])

                        messages.add_message(request, messages.SUCCESS, _('Данные сохранены'))
                        # обновляем ответ на AJAX-запрос, об успешном создании зала
                        self.ajax_content.update({'answer': True})

                    # при добавлении новый целей от пользователя
                    elif request.POST.get('new_body_target_data_id'):
                        # получаем параметр для отслеживания
                        add_target_param = BodyParameter.objects.get(id = request.POST['param_id'])

                        # вводим новое значения параметра
                        TargetBodyParameter.objects.create(target_parameter = add_target_param,
                                                           target_body_data = request.POST['body_target_data'])

                        messages.add_message(request, messages.SUCCESS, _('Данные сохранены'))
                        # обновляем ответ на AJAX-запрос, об успешном создании зала
                        self.ajax_content.update({'answer': True})

                # TODO добавить логгирование ошибок
                except Exception as err:
                    print(err)
                    self.ajax_content.update({'error_answer': _('Произошла ошибка!')})

                finally:
                    return JsonResponse(self.ajax_content)
            else:
                # при удалении отслеживаемого параметра
                if request.POST.get('param_id'):
                    # получаем параметр для отслеживания
                    hide_param = BodyParameter.objects.get(id = request.POST['param_id'])
                    # проверка прав
                    if hide_param.user == fitness_user:
                        # меняем область видимости на False и сохраняем модель
                        hide_param.body_show = False
                        hide_param.save()

                        messages.add_message(request, messages.SUCCESS, _('Данные удалены'))
                    else:

                        messages.add_message(request, messages.ERROR, _('Данные не удалены. Недостаточно прав'))

                # возвращаем пользователя назад на ту же страницу
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:

            messages.add_message(request, messages.ERROR, _('Нехватает прав для просмотра'))
            # возвращаем пользователя назад на ту же страницу
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


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
                                                trainer_price_bargaining = True if request.POST.get('trainer_price_bargaining') else False,
                                                trainer_price_actuality = True if request.POST.get('trainer_price_actuality') else False)

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

                        training_price.trainer_price_bargaining = True if request.POST.get('trainer_price_bargaining') else False

                        training_price.trainer_price_actuality = True if request.POST.get('trainer_price_actuality') else False

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


# trainer data page
class TrainerDataView(View):
    """
    TrainerPriceView отвечает за страницу с расценками тренера,
        а так же создание, редактирование и просмотр расценок тренера
    """
    content = {}
    ajax_content = {'answer': False}

    def get(self, request):
        if request.user.is_authenticated:
            fitness_user = FitnessUser.objects.get(user = request.user)
            # проверка реквеста на AJAX (при получении полных данных о документе тренера)
            if request.is_ajax():
                # запрос на получение информации о документе тренера
                if request.GET.get('trainer_doc_object_id'):
                    # получаем документ тренера
                    trainer_doc = TrainerDoc.objects.get(id = request.GET['trainer_doc_object_id'],
                                                         user__user=fitness_user)

                    self.ajax_content.update({'answer': True,
                                              'trainer_doc_data': {
                                                  'trainer_doc_title': trainer_doc.doc_title
                                              }
                                              }
                                             )

                # запрос на получение информации о документе для последующего редактирования
                elif request.GET.get('edit_doc_id'):
                    # получаем документ тренера
                    trainer_doc = TrainerDoc.objects.get(id = request.GET['edit_doc_id'],
                                                         user__user=fitness_user)

                    self.ajax_content.update({'answer': True,
                                              'trainer_doc_data': {
                                                  'trainer_doc_title': trainer_doc.doc_title,
                                                  'trainer_doc_filename': trainer_doc.filename(),
                                              }
                                              }
                                             )

                return JsonResponse(self.ajax_content)

            # проверка прав доступа к данным страницы
            elif fitness_user.fitness_user_type == FitnessUser.teacher_user:
                self.content.update({
                    'doc': 'pages/personal_area.html',
                    'private_doc': 'pages/trainer_data.html',
                    'fitness_trainer': FitnessTrainer.objects.get(user=fitness_user),
                    'fitness_trainer_docs': TrainerDoc.objects.filter(user__user = fitness_user)})

                return render(request, 'base.html', self.content)

    def post(self, request):
        if request.user.is_authenticated:
            # получаем пользователя от которого пришёл запрос
            fitness_user = FitnessUser.objects.get(user = request.user)

            # создаём новую медицинскую запись запись в дневнике
            if request.POST.get('new_trainer_doc_btn'):
                # создаём новый документ
                TrainerDoc.objects.create(
                    user=FitnessTrainer.objects.get(user = fitness_user),
                    doc_title=request.POST['doc_title'],
                    doc_file=request.FILES['doc_file'])

                # добавляем сообщение для пользователя
                messages.add_message(request, messages.SUCCESS, _('Документ создан'))

            # если удаление дкоумента
            elif request.POST.get('doc_id'):
                # получение документа для удаления
                trainer_doc = TrainerDoc.objects.get(id=request.POST['doc_id'],
                                                     user__user=fitness_user)

                trainer_doc.delete()

                messages.add_message(request, messages.SUCCESS, _('Документ удалён'))

            # возвращаем пользователя назад на ту же страницу
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# change language
class ChangeLanguage(View):
    """
    Класс отвечает за смену языка интерфейса
    """
    def get(self, request, language: str):
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
