from django.contrib.auth.models import Group, User
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.timezone import now
from taggit.managers import TaggableManager
from django.utils.safestring import mark_safe

import datetime
import random
import os


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
    # type пользователя
    teacher_user = "TRN"
    usual_user = "USL"
    fitness_user_type_choice = (
        (teacher_user, 'Trainer'),
        (usual_user, 'Usual'),
    )
    fitness_user_type = models.CharField(max_length=3,
                                         choices=fitness_user_type_choice,
                                         default=usual_user,
                                         verbose_name='user type')
    # фотография пользователя
    image_width = 120
    image_height = 120
    fitness_user_photo = models.ImageField(upload_to = f'profiles_photo/%Y/%m/%d/', default=None,
                                           width_field = 'image_width', height_field = 'image_height',
                                           verbose_name='account photo')
    # gender пользователя
    male_gender = "MAL"
    female_gender = "FEM"
    other_gender = "OTH"
    fitness_user_gender_choice = (
        (male_gender, 'Male'),
        (female_gender, 'Female'),
        (other_gender, 'Other'),
    )
    fitness_user_gender = models.CharField(max_length=3,
                                           choices=fitness_user_gender_choice,
                                           default=male_gender,
                                           verbose_name='user gender')
    # destination city
    fitness_user_destination_city = models.CharField(max_length=50, default='', verbose_name='destination city')

    def image_tag(self):
        return mark_safe(f'<img src="/media/{self.fitness_user_photo}" '
                         f'width="{self.image_width}" height="{self.image_height}" />')
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True

    def __str__(self):
        return f'User: {self.user.username}; User type: {self.get_fitness_user_type_display()}; ' \
               f'User destination: {self.fitness_user_destination_city}'


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
    trainer_description = models.TextField(max_length=5000)

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
    user = models.OneToOneField(FitnessTrainer, on_delete = models.CASCADE)
    # doc title
    doc_title = models.TextField(max_length=1000)
    # doc file
    doc_file = models.FileField(upload_to = f'trainer_docs/%Y/%m/%d/')

    # preview названия документа
    def doc_title_preview(self):
        return f'{self.doc_title[:50]} ...'

    def __str__(self):
        return f'User: {self.user.user.user.username}; Title: {self.doc_title_preview()}'


# trainer prices
class TrainerPrice(models.Model):
    """
    Модель для указания цен тренировки. Не удаляется, а сохраняется для составления статистики цен.
    user - one-to-one с моделью FitnessTrainer
    trainer_price_hour - цена тренировки за час
    trainer_price_currency - валюта в которой указана цена
    trainer_price_creating_datetime - дата создания цены(автоматически задаётся)
    trainer_price_bargaining - возможность торга по цене
    """
    user = models.ForeignKey(FitnessTrainer, on_delete = models.CASCADE)
    # trainer hour price
    trainer_price_hour = models.FloatField()
    # currency
    trainer_price_currency = models.CharField(max_length=20)
    # creating datetime
    trainer_price_creating_datetime = models.DateTimeField(default=now)
    # торги по цене
    trainer_price_bargaining = models.BooleanField(default=True)


# trainer gym
class TrainGym(models.Model):
    """
    Модель для указания залов в которых тренеруется пользователь
    user - foreign-key с моделью FitnessUser
    gym_name - название зала
    gym_description - описание зала
    gym_destination - место расположения зала (страна/город/улица)
    gym_geolocation - точка на карте(json с ключами: latitude/longitude) на которой находится зал
                      (выбирается на гугл-карте, автоматически заполняется `gym_destination` и `gym_name`)
    """
    user = models.ForeignKey(FitnessUser, on_delete = models.CASCADE)
    # gym name
    gym_name = models.CharField(max_length=100)
    # gym full description
    gym_description = models.CharField(max_length=1000)
    # gym destination
    gym_destination = models.CharField(max_length=100)
    # gym geolocation (latitude/longitude)
    gym_geolocation = JSONField(db_index=True, default={'latitude': float(), 'longitude': float()})


# train schedule
class TrainSchedule(models.Model):
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


# list of all settings
class Setting(models.Model):
    """
    Модель для создания списка настроек для всех юзеров.
    setting_title - название настройки
    setting_description - полное описание настройки
    setting_param -  краткое название параметра для фильтрации
    """
    # setting title
    setting_title = models.CharField(max_length=100)
    # description
    setting_description = models.TextField(max_length=1000)
    # param
    setting_param = models.CharField(max_length=30, default='')


# user setting
class UserSetting(models.Model):
    """
    Модель для задания персональных настроек FitnessUser
    user - foreign-key с моделью FitnessUser, для которого применяется настройка.
    user_default_setting - foreign-key с моделью Setting, в которой указывается название настройки.
    setting_data - данные параметра
    """
    user = models.ForeignKey(FitnessUser, on_delete=models.CASCADE)
    # стандартная настройка пользователя
    default_setting = models.ForeignKey(Setting, on_delete=models.CASCADE)
    # персональные данные для настройки
    # data
    setting_data = models.CharField(max_length=100, default='')


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
        (front_view_photo, 'Front'),
        (side_first_view_photo, 'Side first'),
        (side_second_view_photo, 'Side second'),
        (back_view_photo, 'Back'),
    )
    projection_view_type = models.CharField(max_length=3,
                                            choices=projection_view_type_choice,
                                            default=front_view_photo,
                                            verbose_name='projection type')
    # creation datetime
    projection_view_date = models.DateField(default=now)
    # projection photo
    image_width = 120
    image_height = 200
    projection_view_photo = models.ImageField(upload_to = f'projection_view_photo/%Y/%m/%d/', default=None,
                                              width_field = 'image_width', height_field = 'image_height',
                                              verbose_name = 'account photo')

    def image_tag(self):
        return mark_safe(f'<img src="/media/{self.projection_view_photo}" '
                         f'width="{self.image_width}" height="{self.image_height}" />')
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


# user medical note
class MedicalNote(models.Model):
    """
    Модель отвечает за хранение медицинской информации пользователя
    user - foreign-key с моделью FitnessUser, который создаёт медицинскую запись.
    medical_note_title - заголовок записи
    medical_note_text - текст записи
    medical_note_datetime - дата и время создания записи
    medical_note_tags - теги для медицинской записи
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


# user diary
class UserDiary(models.Model):
    """
    Модель отвечает за личный дневник пользователя
    user - foreign-key с моделью FitnessUser, который создаёт запись.
    diary_note_title - заголовок записи
    diary_note_text - текст записи
    diary_note_datetime - дата и время создания записи
    diary_note_tags - теги для записи
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


# train contract
class TrainContract(models.Model):
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
    contract_trainer_agreement = models.BooleanField(default=False)
    # ward agreement
    contract_ward_agreement = models.BooleanField(default=False)
    # hour price
    contract_hour_price = models.FloatField(default=0)
    # payment currency
    contract_currency = models.CharField(max_length=20)
    # success end by trainer
    contract_trainer_end = models.BooleanField(default=False)
    # success end by ward
    contract_ward_end = models.BooleanField(default=False)
    # create datetime
    contract_create_datetime = models.DateTimeField(default=now)
    # expire datetime
    contract_expire_datetime = models.DateTimeField()
    # end datetime
    contract_end_datetime = models.DateTimeField()

















