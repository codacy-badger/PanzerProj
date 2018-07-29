import os
import json

from django.contrib.auth.models import Group, User, BaseUserManager, AbstractBaseUser
from django.contrib.gis.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from taggit.managers import TaggableManager


"""
Files upload functions  
"""


# место для хранения файлов из чата
def chat_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'chat_files/chat_{instance.message_chat.id}/user_{instance.user.user.id}/' \
           f'{now().date().strftime("%Y/%m/%d")}/{filename}'


# место для хранения аватаров
def profile_photo_path(instance, filename):
    return f'profiles_photo/user_{instance.user.id}/{filename}'


# место для хранения документов тренера
def trainer_docs_path(instance, filename):
    return f'trainer_docs/trainer_{instance.user.user.id}/{filename}'


# место для хранения фотографий пользователя в различных проекциях
def projection_photo_path(instance, filename):
    return f'projection_view_photo/user_{instance.user.user.id}/' \
           f'projection_{instance.get_projection_view_type_display()}/' \
           f'{now().date().strftime("%Y/%m/%d")}/{filename}'


"""
User models
"""


# fitness user
class FitnessUser(models.Model):
    """
    Модель для раширения стандартной модели User.
    user - one-to-one с моделью User
    fitness_user_type - тип юзера (тренер/подопечный)
    fitness_user_photo - аватар пользователя
    fitness_user_gender - пол пользователя (М/Ж/неопределился)
    trainer_destination_city - город/местность в которой пользователь находится
    """
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='user_account')
    # birthday date
    fitness_user_bdate = models.DateField(null = True, blank = True)
    # type пользователя
    teacher_user = "TRN"
    ward_user = "WRD"
    fitness_user_type_choice = (
        (teacher_user, _('Тренер')),
        (ward_user, _('Подопечный')),
    )
    fitness_user_type = models.CharField(max_length=3,
                                         choices=fitness_user_type_choice,
                                         default=ward_user,
                                         verbose_name='user type')
    # фотография пользователя
    image_width = 120
    image_height = 120
    fitness_user_photo = models.ImageField(upload_to = profile_photo_path, default=None, blank = True, null = True,
                                           width_field = 'image_width', height_field = 'image_height',
                                           verbose_name='account photo')
    # gender пользователя
    male_gender = "MAL"
    female_gender = "FEM"
    secret_gender = "SEC"
    fitness_user_gender_choice = (
        (male_gender, _('Мужчина')),
        (female_gender, _('Женщина')),
        (secret_gender, _('Секрет')),
    )
    fitness_user_gender = models.CharField(max_length=3,
                                           choices=fitness_user_gender_choice,
                                           default=male_gender,
                                           verbose_name='user gender')
    # destination city
    fitness_user_destination_city = models.CharField(max_length=50, default='', verbose_name='destination city',
                                                     blank = True, null = True)

    def __str__(self):
        return f'User: {self.user.username}; User type: {self.get_fitness_user_type_display()}; ' \
               f'User destination: {self.fitness_user_destination_city}'


"""
Trainer specific models
"""


# trainer account
class FitnessTrainer(models.Model):
    """
    Модель для раширения модели FitnessUser, если пользователь регистрируется как Тренер.
    user - one-to-one с моделью FitnessUser
    trainer_employment_status - занятость тренера (False - не занят, True - занят)
    trainer_description - тренер может оставить краткое описание о себе
    """
    user = models.OneToOneField(FitnessUser, on_delete = models.CASCADE)
    # busy status
    trainer_employment_status = models.BooleanField(default=False)
    # personal description
    trainer_description = models.TextField(max_length=5000, default = 'Description')

    def __str__(self):
        return f'User: {self.user.user.username}; Busy: {self.trainer_employment_status}'


# trainer docs
class TrainerDoc(models.Model):
    """
    Модель для сохранения различных документов(сертификаты/грамоты и прочее) Тренера.
    user - one-to-one с моделью FitnessTrainer
    doc_title - заголовок документа(название и описание документа)
    doc_file - сам документ(файл для скачивания и просмотра)
    """
    user = models.ForeignKey(FitnessTrainer, on_delete = models.CASCADE)
    # doc title
    doc_title = models.TextField(max_length=1000)
    # doc file
    doc_file = models.FileField(upload_to = trainer_docs_path)

    # preview названия документа
    def doc_title_preview(self):
        return self.doc_title if len(self.doc_title) < 50 else self.doc_title[:50]+' ...'

    def filename(self):
        return os.path.basename(self.doc_file.name)

    def __str__(self):
        return f'Trainer: {self.user.user.user.username}; Title: {self.doc_title_preview()}'


# trainer prices
class TrainerPrice(models.Model):
    """
    Модель для указания цен тренировки. Не удаляется, а сохраняется для составления статистики цен.
    user - one-to-one с моделью FitnessTrainer
    trainer_price_hour - цена тренировки за час
    trainer_price_comment - коментарий тренера к цене
    trainer_price_currency - валюта в которой указана цена
    trainer_price_creating_datetime - дата создания цены(автоматически задаётся)
    trainer_price_bargaining - возможность торга по цене
    trainer_price_actuality - актуальность данной цены
    """
    user = models.ForeignKey(FitnessTrainer, on_delete = models.CASCADE)
    # trainer hour price
    trainer_price_hour = models.FloatField()
    # trainer price comment
    trainer_price_comment = models.CharField(max_length = 100, default = '')
    # currency
    trainer_price_currency = models.CharField(max_length=20)
    # creating datetime
    trainer_price_creating_datetime = models.DateTimeField(default=now)
    # торги по цене
    trainer_price_bargaining = models.BooleanField(default=True)
    # price actuality
    trainer_price_actuality = models.BooleanField(default=True)
    # show/hide if trainer delete price
    trainer_price_show = models.BooleanField(default = True)

    def __str__(self):
        return f'Trainer: {self.user.user.user.username}; Price: {self.trainer_price_currency}'


"""
Users gym and schedule models
"""


# trainer gym
class TrainGym(models.Model):
    """
    Модель для указания залов в которых тренеруется пользователь
    user - foreign-key с моделью FitnessUser
    gym_name - название зала
    gym_description - описание зала
    gym_destination - место расположения зала (страна/город/улица)
    gym_geo - точка на карте(latitude/longitude) на которой находится зал
                      (выбирается на карте, автоматически заполняется `gym_destination` и `gym_name`)
    """
    user = models.ForeignKey(FitnessUser, on_delete = models.CASCADE)
    # gym name
    gym_name = models.CharField(max_length=100)
    # gym full description
    gym_description = models.TextField(max_length=1000)
    # gym destination
    gym_destination = models.CharField(max_length=100)
    # gym geo (latitude/longitude)
    gym_geo = models.PointField(geography=True, blank=True, null=True)

    def __str__(self):
        return f'User: {self.user.user.username}; Gym: {self.gym_short_name()}'

    # для вывода краткой информации о зале
    def gym_short_name(self):
        return self.gym_name if len(self.gym_name) < 50 else self.gym_name[:50]+' ...'

    def gym_short_description(self):
        return self.gym_description if len(self.gym_description) < 50 else self.gym_description[:50]+' ...'

    # получение информации о зале в формате JSON
    def get_gym_json(self):
        """
        Получение основной информации о записи и представление её в формате JSON
        gym_user - username автора записи
        gym_name - список тегов записи
        gym_description - текст записи
        gym_destination - название записи
        gym_geo - дата/время создания записи
        :return: JSON  с информацией о записи
        """
        return {
                'gym_user': self.user.user.username,
                'gym_name': self.gym_name,
                'gym_description': self.gym_description,
                'gym_destination': self.gym_destination,
                'gym_geo':{
                    'lat': self.gym_geo.y,
                    'lng': self.gym_geo.x
                    }
                }


# train schedule
class TrainingSchedule(models.Model):
    """
    Модель для указания залов в которых тренерует тренер
    target_user - foreign-key с моделью FitnessUser, для которого составляется расписание
    author_user - foreign-key с моделью FitnessUser, который составил расписание
    schedule_gym - название зала
    schedule_date - дата тренировки
    schedule_train_end - вермя окончания тренеровки
    schedule_train_start - время начала тренеровки
    schedule_train_type - тип тренеровки
    schedule_train_tags - теги для тренировки
    schedule_exercise_set - привязанный к занятию сет упражнений
    """
    target_user = models.ForeignKey(FitnessUser, on_delete = models.CASCADE, related_name='target_schedule_user')
    author_user = models.ForeignKey(FitnessUser, on_delete = models.CASCADE, related_name='author_schedule_user')
    # gym
    schedule_gym = models.ForeignKey(TrainGym, on_delete = models.CASCADE, related_name='schedule_gym')
    # train date
    schedule_date = models.DateField(default=now)
    # train start time
    schedule_train_end = models.TimeField(default=now)
    # train end time
    schedule_train_start = models.TimeField(default=now)
    # train type
    schedule_train_type = models.CharField(max_length=100)
    # train tags
    schedule_train_tags = TaggableManager(blank=True)
    # train set
    schedule_exercise_set = models.ForeignKey('ExerciseSet', on_delete = models.SET_NULL, null = True, blank = True)

    def __str__(self):
        return f'Author: {self.author_user.user.username}; Target: {self.target_user.user.username}; ' \
               f'Gym: {self.schedule_gym.gym_short_name()}; Date: {self.schedule_date}'

    def get_all_tags(self):
        return [tag.name for tag in self.schedule_train_tags.all()]

    # краткое название зала из расписания
    def gym_short(self):
        return self.schedule_gym.gym_short_name()


"""
User settings models
"""


# list of all settings
class Setting(models.Model):
    """
    Модель для создания списка настроек для всех юзеров.
    setting_title - название настройки
    setting_description - полное описание настройки
    setting_param -  краткое название параметра для фильтрации
    """
    # setting title
    setting_title = models.CharField(max_length=100, unique = True)
    # description
    setting_description = models.TextField(max_length=1000)
    # param
    setting_param = models.CharField(max_length=30, default='')

    def short_setting_description(self):
        return self.setting_description if len(self.setting_description) < 50 else self.setting_description[:50]+' ...'

    def __str__(self):
        return f'Title: {self.setting_title}; Param: {self.setting_param}'


# user setting
class UserSetting(models.Model):
    """
    Модель для задания персональных настроек FitnessUser
    user - foreign-key с моделью FitnessUser, для которого применяется настройка.
    default_setting - foreign-key с моделью Setting, в которой указывается название настройки и стандартный параметр.
    setting_data - данные параметра
    """
    user = models.ForeignKey(FitnessUser, on_delete=models.CASCADE)
    # стандартная настройка пользователя
    default_setting = models.ForeignKey(Setting, on_delete=models.CASCADE)
    # персональные данные для настройки
    # data
    setting_data = models.CharField(max_length=100, default='')

    def default_setting_short(self):
        return self.default_setting.setting_title

    def __str__(self):
        return f'User: {self.user.user.username}; Setting: {self.default_setting.setting_title};' \
               f' Param: {self.setting_data}'


"""
Users projections photos model
"""


# user private photos
class ProjectionPhoto(models.Model):
    """
    Модель предназначена для отображения фотографий пользователя по проекциям и дате создания
    user - foreign-key с моделью FitnessUser, который загружает фотографию.
    projection_view_type - тип проекции, передний/боковой_1/боковой_2/задний план
    projection_view_date - дата создания изображения
    projection_view_photo - фотография пользователя в выбранной проекции
    """
    user = models.ForeignKey(FitnessUser, on_delete=models.CASCADE)
    # projection type
    front_view_photo = "FRT"
    side_first_view_photo = "SD1"
    side_second_view_photo = "SD2"
    back_view_photo = "BCK"
    projection_view_type_choice = (
        (front_view_photo, _('Передний вид')),
        (side_first_view_photo, _('Боковой вид №1')),
        (side_second_view_photo, _('Боковой вид №2')),
        (back_view_photo, _('Задний вид')),
    )
    projection_view_type = models.CharField(max_length=3,
                                            choices=projection_view_type_choice,
                                            default=front_view_photo,
                                            verbose_name='projection type')
    # creation datetime
    projection_view_date = models.DateField(default=now)
    # projection photo
    image_width = 100
    image_height = 150
    projection_view_photo = models.ImageField(upload_to = projection_photo_path, default=None,
                                              width_field = 'image_width', height_field = 'image_height',
                                              verbose_name = 'account photo')

    def __str__(self):
        return f'User: {self.user.user.username}; Projection: {self.get_projection_view_type_display()};'


"""
User notes models
"""


# user medical note
class MedicalNote(models.Model):
    """
    Модель отвечает за хранение медицинской информации пользователя
    user - foreign-key с моделью FitnessUser, который создаёт медицинскую запись.
    medical_note_title - заголовок записи
    medical_note_text - текст записи
    medical_note_datetime - дата и время создания записи
    medical_note_tags - теги для медицинской записи
    medical_note_show - скрыть запись, если пользователь удалил её
    """
    user = models.ForeignKey(FitnessUser, on_delete=models.CASCADE)
    # note title
    medical_note_title = models.CharField(max_length=100)
    # note text
    medical_note_text = models.TextField(max_length=4000)
    # creation datetime
    medical_note_datetime = models.DateTimeField(default=now)
    # medical tags
    medical_note_tags = TaggableManager(blank=True)
    # show/hide if user delete diary note
    medical_note_show = models.BooleanField(default = True)

    def short_title(self):
        return self.medical_note_title if len(self.medical_note_title) < 50 else self.medical_note_title[:50]+' ...'

    def short_text(self):
        return self.medical_note_text if len(self.medical_note_text) < 50 else self.medical_note_text[:50]+' ...'

    def get_all_tags(self):
        return [tag.name for tag in self.medical_note_tags.all()]

    # get note main data in JSON format
    def get_note_json(self):
        """
        Получение основной информации о записи и представление её в формате JSON
        diary_note_author - username автора записи
        diary_note_tags - список тегов записи
        diary_note_text - текст записи
        diary_note_title - название записи
        diary_note_datetime - дата/время создания записи
        :return: JSON  с информацией о записи
        """
        return {
                'medical_note_author': self.user.user.username,
                'medical_note_tags': self.get_all_tags(),
                'medical_note_text': self.medical_note_text,
                'medical_note_title': self.medical_note_title,
                'medical_note_datetime': self.medical_note_datetime.strftime("%d %B %Y %H:%M"),
                }

    def __str__(self):
        return f'User: {self.user.user.username}; Title: {self.short_title};'


# user diary
class UserDiary(models.Model):
    """
    Модель отвечает за личный дневник пользователя
    user - foreign-key с моделью FitnessUser, который создаёт запись.
    diary_note_title - заголовок записи
    diary_note_text - текст записи
    diary_note_datetime - дата и время создания записи
    diary_note_tags - теги для записи
    diary_note_show - скрыть запись, если пользователь удалил её
    """
    user = models.ForeignKey(FitnessUser, on_delete=models.CASCADE)
    # note title
    diary_note_title = models.CharField(max_length=100)
    # note text
    diary_note_text = models.TextField(max_length=4000)
    # creation datetime
    diary_note_datetime = models.DateTimeField(default=now)
    # medical tags
    diary_note_tags = TaggableManager(blank=True)
    # show/hide if user delete diary note
    diary_note_show = models.BooleanField(default = True)

    def short_title(self):
        return self.diary_note_title if len(self.diary_note_title) < 30 else self.diary_note_title[:30]+' ...'

    def short_text(self):
        return self.diary_note_text if len(self.diary_note_text) < 30 else self.diary_note_text[:30]+' ...'

    def get_all_tags(self):
        return [tag.name for tag in self.diary_note_tags.all()]

    # get note main data in JSON format
    def get_note_json(self):
        """
        Получение основной информации о записи и представление её в формате JSON
        diary_note_author - username автора записи
        diary_note_tags - список тегов записи
        diary_note_text - текст записи
        diary_note_title - название записи
        diary_note_datetime - дата/время создания записи
        :return: JSON  с информацией о записи
        """
        return {
                'diary_note_author': self.user.user.username,
                'diary_note_tags': self.get_all_tags(),
                'diary_note_text': self.diary_note_text,
                'diary_note_title': self.diary_note_title,
                'diary_note_datetime': self.diary_note_datetime.strftime("%d %B %Y %H:%M"),
                }

    def __str__(self):
        return f'User: {self.user.user.username}; Title: {self.short_title()}...;'


"""
Trainer/Ward contracts and payments models
"""


# train contract
class TrainingContract(models.Model):
    """
    Модель отвечает за создание соглашения между тренером(trainer) и подопечным(ward) для тренировок по определённой
    цене на определённый срок
    contract_trainer_user - foreign-key с моделью FitnessTrainer, который будет выступать тренером.
    contract_ward_user - foreign-key с моделью FitnessUser, который будет выступать подопечным.

    contract_trainer_agreement - согласие тренера на заключение контракта
    contract_ward_agreement - согласие подопечного на заключение контракта

    contract_hour_price - почасовая цена оплаты тренеровки
    contract_currency - валюта оплаты тренеровки

    contract_trainer_end - согласие тренера на закрытие контракта
    contract_ward_end - согласие подопечного на закрытие контракта

    contract_create_datetime - дата создания контракта
    contract_expire_datetime - дата окончания контракта(предполагаемая и задаётся вначале)
    contract_end_datetime - дата реального окончания контракта
    """
    # fitness trainer
    contract_trainer_user = models.ForeignKey(FitnessTrainer, on_delete=models.CASCADE)
    # ward user
    contract_ward_user = models.ForeignKey(FitnessUser, on_delete=models.CASCADE)
    # trainer agreement
    contract_trainer_start = models.BooleanField(default=False)
    # ward agreement
    contract_ward_start = models.BooleanField(default=False)
    # hour price
    contract_hour_price = models.FloatField(default=0)
    # payment currency
    contract_currency = models.CharField(max_length=20)
    # success end by trainer
    contract_trainer_end = models.BooleanField(default=False)
    # success end by ward
    contract_ward_end = models.BooleanField(default=False)
    # create datetime
    contract_create_datetime = models.DateField(default=now)
    # expire datetime
    contract_expire_datetime = models.DateField()
    # end datetime
    contract_end_datetime = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return f'Trainer: {self.contract_trainer_user.user.user.username}; ' \
               f'Ward: {self.contract_ward_user.user.username}'


# train payment
class TrainingPayment(models.Model):
    """
    Модель отвечает за создание платежа между тренером(trainer) и подопечным(target)
    payment_contract - foreign-key с моделью TrainingContract, в которой хранится контракт заключенный между
                        пользователями
    payment_training_schedule - foreign-key с моделью TrainSchedule, в которой хранится занятие созданное по расписанию
                                 в этот временной промежуток (не обязательно к заполнению)

    payment_user_trainer - foreign-key с моделью FitnessTrainer, который будет выступать тренером.
    payment_user_ward - foreign-key с моделью FitnessUser, который будет выступать подопечным.

    payment_training_time - время которое проводилась тренеровка

    payment_price_per_hour - почасовая цена оплаты тренеровки
    payment_currency - валюта оплаты тренеровки

    payment_trainer_success - подтверждение тренера об получении оплаты
    payment_target_success - подтверждение подопечного о совершении оплаты

    payment_create_datetime - дата создания платежа
    payment_expire_datetime - дата окончания возможности погашения платежа
    payment_end_datetime - дата совершения оплаты и подтверждение обеими сторонами
    """
    # contract
    payment_contract = models.ForeignKey(TrainingContract, on_delete=models.CASCADE)
    # train schedule
    payment_training_schedule = models.ForeignKey(TrainingSchedule, on_delete=models.CASCADE, blank=True, null = True)
    # payment user author
    payment_user_trainer = models.ForeignKey(FitnessTrainer, on_delete=models.CASCADE)
    # payment ward user
    payment_user_ward = models.ForeignKey(FitnessUser, on_delete=models.CASCADE)
    # training time
    payment_training_time = models.TimeField()
    # training price per hour
    payment_price_per_hour = models.FloatField()
    # payment currency
    payment_currency = models.CharField(max_length=20)
    # create datetime
    payment_create_datetime = models.DateTimeField(default=now)
    # expire datetime
    payment_expire_datetime = models.DateTimeField()
    # end datetime
    payment_end_datetime = models.DateTimeField(blank = True, null = True)
    # trainer payment success
    payment_trainer_success = models.BooleanField(default=False)
    # target(ward) payment success
    payment_ward_success = models.BooleanField(default=False)

    def __str__(self):
        return f'Trainer: {self.payment_user_trainer.user.user.username}; ' \
               f'Ward: {self.payment_user_ward.user.username}'


"""
User body params models
"""


# user body parameters
class BodyParameter(models.Model):
    """
    Модель предназначена для записи кастомных параметров пользователя
    user - foreign-key с моделью FitnessUser, пользователем который вносит параметр
    body_title - название параметра
    body_data - значение параметра (float)
    body_datetime - дата внесения параметра в список
    """
    user = models.ForeignKey(FitnessUser, on_delete = models.CASCADE)
    # body parameter title
    body_title = models.CharField(max_length = 100)

    def title_short(self):
        return self.body_title if len(self.body_title) < 30 else self.body_title[:30]+' ...'

    def __str__(self):
        return f'User: {self.user.user.username}; ' \
               f'Param title: {self.title_short()}...'

    # получение последней актуальной цели данного параметра
    def actual_target(self):
        return TargetBodyParameter.objects.filter(target_parameter__id = self.id).last()


# user body parameters data
class BodyParameterData(models.Model):
    """
    Модель предназначена для записи кастомных параметров пользователя
    user - foreign-key с моделью FitnessUser, пользователем который вносит параметр
    body_title - название параметра
    body_data - значение параметра (float)
    body_datetime - дата внесения параметра в список
    """
    user_parameter = models.ForeignKey(BodyParameter, on_delete = models.CASCADE)
    # body parameter data
    body_data = models.FloatField()
    # body parameter creating datetime
    body_datetime = models.DateTimeField(default = now)

    def __str__(self):
        return f'User: {self.user_parameter.user.user.username}; ' \
               f'Param title: {self.user_parameter.title_short()}...'

    # форматирование даты+времени в дату
    def datetime_to_date(self):
        return self.body_datetime.strftime("%d %B %Y")

    # получение данных параметра в формате JSON
    def get_parameters_json_data(self):
        # заготовка JSON`a для передачи в графики информации о записанных параметрах пользователя и его целях
        answer = {'user_data': '',
                  'target_data': ''}
        # формирование JSON`a с данными пользователя
        answer.update({'user_data': [{'x': parameter['body_datetime'].strftime("%d %B %Y"), 'y': parameter['body_data']} for parameter in BodyParameterData.objects.filter(user_parameter=self.user_parameter.id).order_by('-body_datetime').values('body_datetime', 'body_data')]})
        # формирование JSON`a с целями пользователя
        answer.update({'target_data': TargetBodyParameter.objects.filter(target_parameter=self.user_parameter.id).last().target_body_data})
        return json.dumps(answer)


# user body parameters
class TargetBodyParameter(models.Model):
    """
    Модель предназначена для записи кастомных ЦЕЛЕЙ параметров пользователя
    user - foreign-key с моделью FitnessUser, пользователем который вносит целевой параметр
    target_body_title - название целевого параметра
    target_body_data - значение целевого параметра (float)
    target_body_datetime - дата создания целевого параметра
    """
    target_parameter = models.ForeignKey(BodyParameter, on_delete = models.CASCADE)
    # target body parameter data
    target_body_data = models.FloatField()
    # body parameter creating datetime
    target_body_datetime = models.DateTimeField(default = now)

    def __str__(self):
        return f'User: {self.target_parameter.user.user.username}; ' \
               f'Target param: {self.target_parameter.title_short()}...'


"""
Chat models
"""


# users chat
class Chat(models.Model):
    """
    Модель отвечает за чат между двумя пользователями
    users - пользователи принимающие участие в чате
    chat_alive - доступность чата(если один из пользователей заблокировал его, то никто не сможет писать)
    """
    users = models.ManyToManyField(FitnessUser)
    # chat alive
    chat_alive = models.BooleanField(default = True)

    def users_list(self):
        return [participant.user.username for participant in self.users.all()]

    users_list.short_description = 'Participants names'

    def __str__(self):
        return f'Users: {self.users_list()}; Alive: {self.chat_alive}'


# chat message
class ChatMessage(models.Model):
    """
    Модель отвечает за сообщение пользователя
    user - автор сообщения
    message_chat - чат в который было отправлено сообщение
    message_text - текст сообщения
    message_file - файл в сообщении (необязательное поле)
    """
    # message author
    user = models.ForeignKey(FitnessUser, on_delete = models.CASCADE)
    # chat
    message_chat = models.ForeignKey(Chat, on_delete = models.CASCADE)
    # message text
    message_text = models.TextField(max_length = 1000)
    # message creating datetime
    message_datetime = models.DateTimeField(default = now)
    # message read status
    message_readed = models.BooleanField(default = False)
    # message file
    message_file = models.FileField(blank = True, null = True, upload_to = chat_directory_path)

    def __str__(self):
        return f'User: {self.user.user.username}; Chat: {self.message_chat.users_list()}; ' \
               f'Message: {self.short_message()}'

    def short_message(self):
        return self.message_text if len(self.message_text) < 30 else self.message_text[:30] + ' ...'


"""
Feedback model 
"""


# users feed-backs
class Feedback(models.Model):
    """
    Модель отвечает за фидбеки пользователей после заключения/окончания контракта
    target_user - FitnessUser на которого пишется фидбэк
    author_user - FitnessUser который написал фидбэк
    feedback_title - тема фидбэка
    feedback_text - текст фидбэка
    feedback_rate - рейтинг поставленный одним пользователем, другому
    feedback_datetime - дата создания фидбэка
    """
    # target user
    target_user = models.ForeignKey(FitnessUser, on_delete = models.CASCADE, related_name='target_feedback_user')
    # feedback author user
    author_user = models.ForeignKey(FitnessUser, on_delete = models.CASCADE, related_name='author_feedback_user')
    # title
    feedback_title = models.CharField(max_length = 100)
    # text
    feedback_text = models.TextField(max_length = 4000)
    # rate
    feedback_rate = models.FloatField(default = 0)
    # datetime
    feedback_datetime = models.DateTimeField(default = now)

    def __str__(self):
        return f'Target: {self.target_user.user.username}; Rate: {self.feedback_rate}'

    def short_title(self):
        return self.feedback_title if len(self.feedback_title) < 30 else self.feedback_title[:30]+' ...'

    def short_text(self):
        return self.feedback_text if len(self.feedback_text) < 30 else self.feedback_text[:30]+' ...'


"""
Default exercise models
"""


# default exercise type
class DefExerciseType(models.Model):
    """
    Модель отвечает за хранение стандартных типов упражнений
    type_title - название типа упражнения
    type_description - описание типа упражнения
    """
    # default type title
    type_title = models.CharField(max_length = 100)
    # default type description
    type_description = models.TextField(max_length=5000)

    def short_title(self):
        return self.type_title if len(self.type_title) < 30 else self.type_title[:30]+' ...'

    def short_description(self):
        return self.type_description if len(self.type_description) < 30 else self.type_description[:30]+' ...'

    def __str__(self):
        return f'Title: {self.short_title()}'


# default type/subtype bundle
class DefTypesBundle(models.Model):
    """
    Модель отвечает за хранение стандартных связей между типами/подтипами упражнений
    bundle_type - тип упражнения
    bundle_subtypes - подтипы данного типа упражнения
    """
    # bundled exercise type
    bundle_type = models.ForeignKey(DefExerciseType, on_delete = models.SET_NULL, null = True, blank = True,
                                    related_name = 'bundled_type')
    # bundled exercises subtypes
    bundle_subtypes = models.ManyToManyField(DefExerciseType, blank = True, related_name = 'bundled_subtypes')

    def short_type(self):
        return self.bundle_type.type_title if len(self.bundle_type.type_title) < 30 \
                                           else self.bundle_type.type_title[:30]+' ...'

    def get_bundled_types(self):
        return [type_title.short_title() for type_title in self.bundle_subtypes.all()]

    def __str__(self):
        return f'Type: {self.short_type()}; Subtypes: {self.get_bundled_types()}'


# default exercises model
class DefExercise(models.Model):
    """
    Модель отвечает за хранение стандартных упражнений
    exercise_type - тип к которому относится упражнение
    exercise_title - название упражнения
    exercise_description - описание упражнения
    exercise_approaches - кол-во подходов данного упражнения
    exercise_set - сеты в которые включено данное упражнение
    """
    # default exercise type
    exercise_type = models.ForeignKey(DefExerciseType, on_delete = models.SET_NULL, null = True, blank = True)
    # default exercise title
    exercise_title = models.CharField(max_length = 100)
    # default exercise description
    exercise_description = models.TextField(max_length=5000)
    # default approaches number
    exercise_approaches = models.IntegerField(default = 0, blank = True, null = True)

    def short_title(self):
        return self.exercise_title if len(self.exercise_title) < 50 else self.exercise_title[:50]+' ...'

    def short_description(self):
        return self.exercise_description if len(self.exercise_description) < 50 \
                                         else self.exercise_description[:50]+' ...'

    def __str__(self):
        return f'Title: {self.short_title()}'


"""
Users exercise models
"""


# exercise type
class ExerciseType(models.Model):
    """
    Модель отвечает за хранение пользовательских типов упражнений
    type_title - название типа упражнения
    type_description - описание типа упражнения
    type_datetime - дата создания типа
    """
    # user owner
    type_owner = models.ForeignKey(FitnessUser, on_delete = models.CASCADE)
    # type title
    type_title = models.CharField(max_length = 100)
    # type description
    type_description = models.TextField(max_length=5000)
    # create datetime
    type_datetime = models.DateTimeField(default = now)

    def short_title(self):
        return self.type_title if len(self.type_title) < 50 else self.type_title[:50]+' ...'

    def short_description(self):
        return self.type_description if len(self.type_description) < 50 else self.type_description[:50]+' ...'

    def __str__(self):
        return f'Title: {self.short_title()}'


# type/subtype bundle
class TypesBundle(models.Model):
    """
    Модель отвечает за хранение пользовательских связей между типами/подтипами упражнений
    bundle_type - тип упражнения
    bundle_subtypes - подтипы данного типа упражнения
    bundle_datetime - дата создания связи
    """
    # bundled exercise type
    bundle_type = models.ForeignKey(ExerciseType, on_delete = models.SET_NULL, null = True, blank = True,
                                    related_name = 'bundled_type')
    # bundled exercises subtypes
    bundle_subtypes = models.ManyToManyField(ExerciseType, blank = True, related_name = 'bundled_subtypes')
    # bundle creating datetime
    bundle_datetime = models.DateTimeField(default = now)

    def short_type(self):
        return self.bundle_type.type_title if len(self.bundle_type.type_title) < 50 \
                                           else self.bundle_type.type_title[:50]+' ...'

    def get_bundled_types(self):
        return [type_title.short_title() for type_title in self.bundle_subtypes.all()]

    def __str__(self):
        return f'Type: {self.short_type()}; Subtypes: {self.get_bundled_types()}'


# exercises model
class Exercise(models.Model):
    """
    Модель отвечает за хранение пользовательских упражнений
    exercise_owner - владелец упражнения
    exercise_type - тип к которому относится упражнение
    exercise_title - название упражнения
    exercise_description - описание упражнения
    exercise_approaches - кол-во подходов данного упражнения
    exercise_datetime - дата создания упражнения
    """
    # user owner
    exercise_owner = models.ForeignKey(FitnessUser, on_delete = models.CASCADE)
    # default exercise type
    exercise_type = models.ForeignKey(ExerciseType, on_delete = models.SET_NULL, null = True, blank = True)
    # default exercise title
    exercise_title = models.CharField(max_length = 100)
    # default exercise description
    exercise_description = models.TextField(max_length=5000)
    # default approaches number
    exercise_approaches = models.IntegerField(default = 0, blank = True, null = True)
    # create datetime
    exercise_datetime = models.DateTimeField(default = now)

    def short_title(self):
        return self.exercise_title if len(self.exercise_title) < 50 else self.exercise_title[:50]+' ...'

    def short_description(self):
        return self.exercise_description if len(self.exercise_description) < 50 \
                                         else self.exercise_description[:50]+' ...'

    def __str__(self):
        return f'Title: {self.short_title()}; Type: {self.exercise_type.short_title()}'


"""
Exercises set
"""


# exercises set model
class ExerciseSet(models.Model):
    """
    Модель отвечает за хранение сетов упражнений пользователя
    set_owner - владелец сета
    set_exercises - пользовательские упражнения в сете
    set_title - название сета
    set_description - полное описание сета
    set_def_exercises - стандартные упражнения в сете
    set_datetime - дата создания сета
    """
    # set owner
    set_owner = models.ForeignKey(FitnessUser, on_delete = models.CASCADE)
    # set title
    set_title = models.CharField(max_length = 100)
    # set description
    set_description = models.TextField(max_length = 5000)
    # set exercises
    set_exercises = models.ManyToManyField(Exercise, blank = True)
    # set default exercises
    set_def_exercises = models.ManyToManyField(DefExercise, blank = True)
    # create datetime
    set_datetime = models.DateTimeField(default = now)

    def short_title(self):
        return self.set_title if len(self.set_title) < 50 else self.set_title[:50]+' ...'

    def short_description(self):
        return self.set_description if len(self.set_description) < 50 else self.set_description[:50]+' ...'

    def get_set_exercises(self):
        return [type_title.short_title() for type_title in self.set_exercises.all()]

    def get_set_def_exercises(self):
        return [type_title.short_title() for type_title in self.set_def_exercises.all()]

    def __str__(self):
        return f'Title: {self.short_title()}; Owner: {self.set_owner.user.username}'


"""
Share models
"""


# shared exercise model
class SharedExercise(models.Model):
    """
    Модель отвечает за хранение расшаренных пользователем упражнений
    shared_exercise - упражнение которое расшарил пользователь
    shared_rate - рейтинг расшаренного упражнения
    shared_copies - кол-во копий данного упражнения
    shared_datetime - дата создания данного расшаренного упражнения
    """
    # shared exercises
    shared_exercise = models.OneToOneField(Exercise, on_delete = models.CASCADE)
    # share exercise rate
    shared_rate = models.FloatField(default = 0)
    # copies taken
    shared_copies = models.IntegerField(default = 0)
    # create datetime
    shared_datetime = models.DateTimeField(default = now)

    def __str__(self):
        return f'Exercise: {self.shared_exercise.short_title()}; Rate: {self.shared_rate}'


# shared exercises set model
class SharedSet(models.Model):
    """
    Модель отвечает за хранение расшаренных пользователем сетов упражнений
    shared_set - сет, который расшарил пользователь
    shared_rate - рейтинг сета
    shared_copies - кол-во копий сета
    shared_datetime  - дата создания сета
    """
    # shared sets
    shared_set = models.OneToOneField(ExerciseSet, on_delete = models.CASCADE)
    # share set rate
    shared_rate = models.FloatField(default = 0)
    # copies taken
    shared_copies = models.IntegerField(default = 0)
    # create datetime
    shared_datetime = models.DateTimeField(default = now)

    def __str__(self):
        return f'Set: {self.shared_set.short_title()}; Rate: {self.shared_rate}'











