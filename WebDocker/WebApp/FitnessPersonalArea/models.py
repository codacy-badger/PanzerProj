from django.contrib.auth.models import Group, User
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.timezone import now
from taggit.managers import TaggableManager


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
        return f'Trainer: {self.user.user.user.username}; Title: {self.doc_title_preview()}'


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

    def __str__(self):
        return f'Trainer: {self.user.user.user.username}; Price: {self.trainer_price_currency}'


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
    gym_description = models.TextField(max_length=1000)
    # gym destination
    gym_destination = models.CharField(max_length=100)
    # gym geolocation (latitude/longitude)
    gym_geolocation = JSONField(db_index=True, default={'latitude': float(), 'longitude': float()})

    def __str__(self):
        return f'User: {self.user.user.username}; Gym: {self.gym_short_name()}'

    # для вывода краткой информации о зале
    def gym_short_name(self):
        if len(self.gym_name) > 50:
            return f'{self.gym_name[:50]}...'
        else:
            return self.gym_name

    def gym_short_description(self):
        if len(self.gym_description) > 50:
            return f'{self.gym_description[:50]}...'
        else:
            return self.gym_description


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

    def __str__(self):
        return f'Author: {self.author_user.user.username}; Target: {self.target_user.user.username}; ' \
               f'Gym: {self.schedule_gym.gym_short_name()}; Date: {self.schedule_date}'

    def get_all_tags(self):
        return self.schedule_train_tags.all()

    # краткое название зала из расписания
    def gym_short(self):
        return self.schedule_gym.gym_short_name()


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
        if len(self.setting_description) > 50:
            return f'{self.setting_description[:50]}...'
        else:
            return self.setting_description

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
    image_width = 100
    image_height = 150
    projection_view_photo = models.ImageField(upload_to = f'projection_view_photo/%Y/%m/%d/', default=None,
                                              width_field = 'image_width', height_field = 'image_height',
                                              verbose_name = 'account photo')

    def __str__(self):
        return f'User: {self.user.user.username}; Projection: {self.get_projection_view_type_display()};'


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

    def short_title(self):
        if len(self.medical_note_title) > 50:
            return f'{self.medical_note_title[:50]}...'
        else:
            return self.medical_note_title

    def get_all_tags(self):
        return self.medical_note_tags.all()

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

    def short_title(self):
        if len(self.diary_note_title) > 50:
            return f'{self.diary_note_title[:50]}...'
        else:
            return self.diary_note_title

    def get_all_tags(self):
        return self.diary_note_tags.all()

    def __str__(self):
        return f'User: {self.user.user.username}; Title: {self.short_title()}...;'


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
    contract_create_datetime = models.DateTimeField(default=now)
    # expire datetime
    contract_expire_datetime = models.DateTimeField()
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
    payment_user_target - foreign-key с моделью FitnessUser, который будет выступать подопечным.

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
    # body parameter data
    body_data = models.FloatField()
    # body parameter creating datetime
    body_datetime = models.DateTimeField(default = now)

    def title_short(self):
        if len(self.body_title) > 50:
            return f'{self.body_title[:50]}...'
        else:
            return self.body_title

    def __str__(self):
        return f'User: {self.user.user.username}; ' \
               f'Param title: {self.title_short()}...'


# user body parameters
class TargetBodyParameter(models.Model):
    """
    Модель предназначена для записи кастомных ЦЕЛЕЙ параметров пользователя
    user - foreign-key с моделью FitnessUser, пользователем который вносит целевой параметр
    target_body_title - название целевого параметра
    target_body_data - значение целевого параметра (float)
    target_body_datetime - дата создания целевого параметра
    """
    user = models.ForeignKey(FitnessUser, on_delete = models.CASCADE)
    # target body parameter title
    target_body_title = models.CharField(max_length = 100)
    # target body parameter data
    target_body_data = models.FloatField()
    # body parameter creating datetime
    target_body_datetime = models.DateTimeField(default = now)

    def title_short(self):
        if len(self.target_body_title) > 50:
            return f'{self.target_body_title[:50]}...'
        else:
            return self.target_body_title

    def __str__(self):
        return f'User: {self.user.user.username}; ' \
               f'Target param: {self.title_short()}...'










