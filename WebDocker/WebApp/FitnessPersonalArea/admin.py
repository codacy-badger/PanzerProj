from django.contrib import admin

from .models import FitnessUser, FitnessTrainer, TrainerDoc, TrainerPrice, TrainGym, TrainingSchedule, Setting, \
    UserSetting, ProjectionPhoto, MedicalNote, UserDiary, TrainingContract, TrainingPayment, BodyParameter, TargetBodyParameter


#  класс для кастомизации модели FitnessUser (общей модели юзера)
class ExtendedFitnessUser(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('user', 'fitness_user_type', 'fitness_user_gender', 'fitness_user_destination_city', 'image_tag')
    # поля для поиска
    search_fields = ('id', 'user__id', 'user__username', 'fitness_user_gender', 'fitness_user_destination_city',
                     'fitness_user_type')
    # поля для фильтрации
    list_filter = ('user__is_active', 'user__last_login', 'user__date_joined', 'fitness_user_type',
                   'fitness_user_gender')


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedFitnessTrainer(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('user_short', 'trainer_employment_status', 'trainer_description')
    # поля для поиска
    search_fields = ('id', 'user__user__id', 'user__user__username', 'trainer_employment_status', 'trainer_description')
    # поля для фильтрации
    list_filter = ('user__user__is_active', 'user__user__last_login', 'user__user__date_joined',
                   'trainer_employment_status')


#  класс для кастомизации модели TrainerDocs (раширения модели медицинских записей)
class ExtendedTrainerDocs(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('user_short', 'doc_title_preview', 'doc_file')
    # поля для поиска
    search_fields = ('id', 'user__user__id', 'user__user__username', 'doc_title')
    # поля для фильтрации
    list_filter = ('user__user__user__is_active', 'user__user__user__last_login', 'user__user__user__date_joined')


#  класс для кастомизации модели TrainerPrice (раширения модели цены тренесркой работы)
class ExtendedTrainerPrice(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('user_short', 'trainer_price_hour', 'trainer_price_currency', 'trainer_price_creating_datetime',
                    'trainer_price_bargaining')
    # поля для поиска
    search_fields = ('id', 'user__user__id', 'user__user__username', 'trainer_price_hour', 'trainer_price_currency')
    # поля для фильтрации
    list_filter = ('user__user__user__is_active', 'user__user__user__last_login', 'user__user__user__date_joined',
                   'trainer_price_bargaining', 'trainer_price_currency')


#  класс для кастомизации модели ExtendedTrainGym (раширения модели для описания зала)
class ExtendedTrainGym(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('user_short', 'gym_short_name', 'gym_short_description', 'gym_destination')
    # поля для поиска
    search_fields = ('id', 'user__user__id', 'user__user__username', 'gym_name', 'gym_description', 'gym_destination')
    # поля для фильтрации
    list_filter = ('user__user__is_active', 'user__user__last_login', 'user__user__date_joined')


#  класс для кастомизации модели TrainingSchedule (раширения модели расписания тренировок)
class ExtendedTrainingSchedule(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('target_user_short', 'author_user_short', 'gym_short', 'get_all_tags')
    # поля для поиска
    search_fields = ('user__user__username', 'gym_name', 'gym_description', 'gym_destination')


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedSetting(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('setting_title', 'short_setting_description', 'setting_param')
    # поля для поиска
    search_fields = ('id', 'setting_title', 'setting_description')


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedUserSetting(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('user_short', 'default_setting_short', 'setting_data')
    # поля для поиска
    search_fields = ('id', 'user__user__id', 'user__user__username', 'default_setting_short')
    # поля для фильтрации
    list_filter = ('user__user__is_active', 'user__user__last_login', 'user__user__date_joined',
                   'default_setting__setting_title')


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedProjectionPhoto(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('user_short', 'projection_view_type', 'image_tag')
    # поля для поиска
    search_fields = ('id', 'user__user__id', 'user__user__username')
    # поля для фильтрации
    list_filter = ('user__user__is_active', 'user__user__last_login', 'user__user__date_joined', 'projection_view_type',
                   'projection_view_date')


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedMedicalNote(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('user_short', 'short_title', 'medical_note_datetime', 'get_all_tags')
    # поля для поиска
    search_fields = ('id', 'user__user__id', 'user__user__username')
    # поля для фильтрации
    list_filter = ('user__user__is_active', 'user__user__last_login', 'user__user__date_joined', 'medical_note_datetime')


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedUserDiary(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('user_short', 'short_title', 'diary_note_datetime', 'get_all_tags')
    # поля для поиска
    search_fields = ('id', 'user__user__id', 'user__user__username')
    # поля для фильтрации
    list_filter = ('user__user__is_active', 'user__user__last_login', 'user__user__date_joined', 'diary_note_datetime')


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedTrainingContract(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('trainer_user_short', 'ward_user_short', 'contract_trainer_start', 'contract_ward_start',
                    'contract_trainer_end', 'contract_ward_end', 'contract_create_datetime', 'contract_expire_datetime',
                    'contract_end_datetime')
    # поля для поиска
    search_fields = ('id', 'contract_trainer_user__user__user__id', 'contract_trainer_user__user__user__username')
    # поля для фильтрации
    list_filter = ('contract_trainer_start', 'contract_ward_start', 'contract_trainer_end', 'contract_ward_end')


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedTrainingPayment(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('trainer_user_short', 'ward_user_short', 'payment_contract', 'payment_training_time',
                    'payment_price_per_hour', 'payment_currency', 'payment_create_datetime',
                    'payment_expire_datetime', 'payment_end_datetime', 'payment_trainer_success',
                    'payment_ward_success')
    # поля для поиска
    search_fields = ('id', 'payment_user_trainer__user__user__id', 'payment_user_target__user__user__username')
    # поля для фильтрации
    list_filter = ('payment_currency', 'payment_trainer_success', 'payment_ward_success')


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedBodyParameter(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('user_short', 'title_short', 'body_data', 'body_datetime')
    # поля для поиска
    search_fields = ('id', 'user__user__id', 'user__user__username', 'body_title')
    # поля для фильтрации
    list_filter = ('body_datetime',)


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedTargetBodyParameter(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('user_short', 'title_short', 'target_body_data', 'target_body_datetime')
    # поля для поиска
    search_fields = ('id', 'user__user__id', 'user__user__username', 'target_body_title')
    # поля для фильтрации
    list_filter = ('target_body_datetime',)


admin.site.register(FitnessUser, ExtendedFitnessUser)
admin.site.register(FitnessTrainer, ExtendedFitnessTrainer)
admin.site.register(TrainerDoc, ExtendedTrainerDocs)
admin.site.register(TrainerPrice, ExtendedTrainerPrice)
admin.site.register(TrainGym, ExtendedTrainGym)
admin.site.register(TrainingSchedule, ExtendedTrainingSchedule)
admin.site.register(Setting, ExtendedSetting)
admin.site.register(UserSetting, ExtendedUserSetting)
admin.site.register(ProjectionPhoto, ExtendedProjectionPhoto)
admin.site.register(MedicalNote, ExtendedMedicalNote)
admin.site.register(UserDiary, ExtendedUserDiary)
admin.site.register(TrainingContract, ExtendedTrainingContract)
admin.site.register(TrainingPayment, ExtendedTrainingPayment)
admin.site.register(BodyParameter, ExtendedBodyParameter)
admin.site.register(TargetBodyParameter, ExtendedTargetBodyParameter)










