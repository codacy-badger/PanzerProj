from django.contrib.auth.models import Group, User
from django.contrib.postgres.fields import JSONField
from django.db import models
from taggit.managers import TaggableManager
from django.utils.timezone import now
from django.db.models import Q

import datetime
import random
import time


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
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    # type пользователя
    teacher_user = "TRN"
    usual_user = "USL"
    fitness_user_type_choice = (
        (teacher_user, 'Trainer'),
        (usual_user, 'Usual'),
    )
    fitness_user_type = models.CharField(max_length=3,
                                         choices=fitness_user_type_choice,
                                         default=usual_user)
    # фотография пользователя
    image_width = 50
    image_height = 50
    fitness_user_photo = models.ImageField(upload_to = f'profiles_photo/%Y/%m/%d/', default=None,
                                           width_field = 'image_width', height_field = 'image_height')
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
                                           default=male_gender)
    # destination city
    fitness_user_destination_city = models.CharField(max_length=50, default='')


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
    trainer_description = models.CharField(max_length=5000)


# trainer docs
class TrainerDocs(models.Model):
    """
    Модель для сохранения различных документов(сертификаты/грамоты и прочее) Тренера.
    user - one-to-one с моделью FitnessTrainer
    doc_title - заголовок документа(название и описание документа)
    doc_file - сам документ(файл для скачивания и просмотра)
    """
    user = models.OneToOneField(FitnessTrainer, on_delete = models.CASCADE)
    # doc title
    doc_title = models.CharField(max_length=1000)
    # doc file
    doc_file = models.FileField(upload_to = f'trainer_docs/%Y/%m/%d/')


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
    user = models.OneToOneField(FitnessTrainer, on_delete = models.CASCADE)
    # trainer hour price
    trainer_price_hour = models.FloatField()
    # currency
    trainer_price_currency = models.CharField(max_length=20)
    # creating datetime
    trainer_price_creating_datetime = models.DateTimeField(default=now)
    # торги по цене
    trainer_price_bargaining = models.BooleanField(default=True)


# trainer gym
class TrainerGym(models.Model):
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
    """
    target_user = models.ForeignKey(FitnessUser, on_delete = models.CASCADE, related_name='target_schedule_user')
    author_user = models.ForeignKey(FitnessUser, on_delete = models.CASCADE, related_name='author_schedule_user')
    # gym
    schedule_gym = models.ForeignKey(TrainerGym, on_delete = models.CASCADE, related_name='schedule_gym')
    # train date
    schedule_date = models.DateField(default=now)
    # train start time
    schedule_train_end = models.TimeField(default=now)
    # train end time
    schedule_train_start = models.TimeField(default=now)
    # train type
    schedule_train_type = models.CharField(max_length=100)












