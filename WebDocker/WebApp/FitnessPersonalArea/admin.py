from django.contrib import admin

from .models import FitnessUser, FitnessTrainer, TrainerDoc, TrainerPrice, TrainGym, TrainSchedule, Setting, UserSetting


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
    list_display = ('user', 'trainer_employment_status', 'trainer_description')
    # поля для поиска
    search_fields = ('id', 'user__user__id', 'user__user__username', 'trainer_employment_status', 'trainer_description')
    # поля для фильтрации
    list_filter = ('user__user__is_active', 'user__user__last_login', 'user__user__date_joined',
                   'trainer_employment_status')


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedTrainerDocs(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('user', 'doc_title_preview', 'doc_file')
    # поля для поиска
    search_fields = ('id', 'user__user__id', 'user__user__username', 'doc_title')
    # поля для фильтрации
    list_filter = ('user__user__user__is_active', 'user__user__user__last_login', 'user__user__user__date_joined')


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedTrainerPrice(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('user', 'trainer_price_hour', 'trainer_price_currency', 'trainer_price_creating_datetime',
                    'trainer_price_bargaining')
    # поля для поиска
    search_fields = ('id', 'user__user__id', 'user__user__username', 'trainer_price_hour', 'trainer_price_currency')
    # поля для фильтрации
    list_filter = ('user__user__user__is_active', 'user__user__user__last_login', 'user__user__user__date_joined',
                   'trainer_price_bargaining', 'trainer_price_currency')


admin.site.register(FitnessUser, ExtendedFitnessUser)
admin.site.register(FitnessTrainer, ExtendedFitnessTrainer)
admin.site.register(TrainerDoc, ExtendedTrainerDocs)
admin.site.register(TrainerPrice, ExtendedTrainerPrice)











