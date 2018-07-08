from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import FitnessUser, FitnessTrainer, TrainerDoc, TrainerPrice, TrainGym, TrainingSchedule, Setting, \
    UserSetting, ProjectionPhoto, MedicalNote, UserDiary, TrainingContract, TrainingPayment, BodyParameter, \
    TargetBodyParameter, Chat, ChatMessage, Feedback, DefExerciseType, DefTypesBundle, DefExercise, ExerciseType,\
    TypesBundle, Exercise, ExerciseSet, SharedExercise, SharedSet


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

    def image_tag(self, obj):
        return mark_safe(f'<img src="/media/{obj.fitness_user_photo}" '
                         f'width="{obj.image_width}" height="{obj.image_height}" />')

    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedFitnessTrainer(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('user_short', 'trainer_employment_status', 'trainer_description')
    # поля для поиска
    search_fields = ('id', 'user__user__id', 'user__user__username', 'trainer_employment_status', 'trainer_description')
    # поля для фильтрации
    list_filter = ('user__user__is_active', 'user__user__last_login', 'user__user__date_joined',
                   'trainer_employment_status')

    # для вывода в username
    def user_short(self, obj):
        return obj.user.user.username

    user_short.short_description = 'User name'


#  класс для кастомизации модели TrainerDocs (раширения модели медицинских записей)
class ExtendedTrainerDocs(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('user_short', 'doc_title_preview', 'doc_file')
    # поля для поиска
    search_fields = ('user__user__user__username', 'doc_title')
    # поля для фильтрации
    list_filter = ('user__user__user__is_active', 'user__user__user__last_login', 'user__user__user__date_joined')

    # для вывода в username
    def user_short(self, obj):
        return obj.user.user.user.username

    user_short.short_description = 'User name'


#  класс для кастомизации модели TrainerPrice (раширения модели цены тренесркой работы)
class ExtendedTrainerPrice(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('user_short', 'trainer_price_hour', 'trainer_price_currency', 'trainer_price_creating_datetime',
                    'trainer_price_bargaining', 'trainer_price_actuality')
    # поля для поиска
    search_fields = ('user__user__user__username', )
    # поля для фильтрации
    list_filter = ('user__user__user__is_active', 'user__user__user__last_login', 'user__user__user__date_joined',
                   'trainer_price_bargaining', 'trainer_price_currency', 'trainer_price_actuality')

    # для вывода в username
    def user_short(self, obj):
        return obj.user.user.user.username

    user_short.short_description = 'User name'


#  класс для кастомизации модели ExtendedTrainGym (раширения модели для описания зала)
class ExtendedTrainGym(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('user_short', 'gym_short_name', 'gym_short_description', 'gym_destination')
    # поля для поиска
    search_fields = ('id', 'user__user__id', 'user__user__username', 'gym_name', 'gym_description', 'gym_destination')
    # поля для фильтрации
    list_filter = ('user__user__is_active', 'user__user__last_login', 'user__user__date_joined')

    # для вывода в username
    def user_short(self, obj):
        return obj.user.user.username

    user_short.short_description = 'User name'


#  класс для кастомизации модели TrainingSchedule (раширения модели расписания тренировок)
class ExtendedTrainingSchedule(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('target_user_short', 'author_user_short', 'gym_short', 'get_all_tags')
    # поля для поиска
    search_fields = ('target_user__user__username', 'author_user__user__username', 'schedule_gym__gym_name',
                     'schedule_gym__gym_description', 'schedule_train_type')

    # для вывода в username
    def target_user_short(self, obj):
        return obj.target_user.user.username

    def author_user_short(self, obj):
        return obj.author_user.user.username

    target_user_short.short_description = 'Target name'
    author_user_short.short_description = 'Author name'


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
    search_fields = ('user__user__username', 'default_setting__setting_description', 'default_setting__setting_title',
                     'setting_data')
    # поля для фильтрации
    list_filter = ('user__user__is_active', 'user__user__last_login', 'user__user__date_joined',
                   'default_setting__setting_title')

    def user_short(self, obj):
        return obj.user.user.username

    user_short.short_description = 'User name'


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedProjectionPhoto(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('user_short', 'projection_view_type', 'image_tag')
    # поля для поиска
    search_fields = ('id', 'user__user__id', 'user__user__username')
    # поля для фильтрации
    list_filter = ('user__user__is_active', 'user__user__last_login', 'user__user__date_joined', 'projection_view_type',
                   'projection_view_date')

    def image_tag(self, obj):
        return mark_safe(f'<img src="/media/{obj.projection_view_photo}" '
                         f'width="{obj.image_width}" height="{obj.image_height}" />')

    def user_short(self, obj):
        return obj.user.user.username

    user_short.short_description = 'User name'
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedMedicalNote(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('user_short', 'short_title', 'medical_note_datetime', 'get_all_tags')
    # поля для поиска
    search_fields = ('id', 'user__user__id', 'user__user__username')
    # поля для фильтрации
    list_filter = ('user__user__is_active', 'user__user__last_login', 'user__user__date_joined', 'medical_note_datetime')

    def user_short(self, obj):
        return obj.user.user.username

    user_short.short_description = 'User name'


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedUserDiary(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('user_short', 'short_title', 'diary_note_datetime', 'get_all_tags')
    # поля для поиска
    search_fields = ('id', 'user__user__id', 'user__user__username')
    # поля для фильтрации
    list_filter = ('user__user__is_active', 'user__user__last_login', 'user__user__date_joined', 'diary_note_datetime')

    def user_short(self, obj):
        return obj.user.user.username

    user_short.short_description = 'User name'


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedTrainingContract(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('trainer_short_name', 'ward_short_name', 'contract_trainer_start', 'contract_ward_start',
                    'contract_trainer_end', 'contract_ward_end', 'contract_create_datetime', 'contract_expire_datetime',
                    'contract_end_datetime')
    # поля для поиска
    search_fields = ('id', 'contract_trainer_user__user__user__id', 'contract_trainer_user__user__user__username')
    # поля для фильтрации
    list_filter = ('contract_trainer_start', 'contract_ward_start', 'contract_trainer_end', 'contract_ward_end')

    def ward_short_name(self, obj):
        return obj.contract_ward_user.user.username

    def trainer_short_name(self, obj):
        return obj.contract_trainer_user.user.user.username

    # переименование полей для отображения
    trainer_short_name.short_description = 'Trainer name'
    ward_short_name.short_description = 'Ward name'


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedTrainingPayment(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('trainer_user_short', 'ward_user_short', 'payment_contract', 'payment_training_time',
                    'payment_price_per_hour', 'payment_currency', 'payment_create_datetime',
                    'payment_expire_datetime', 'payment_end_datetime', 'payment_trainer_success',
                    'payment_ward_success')
    # поля для поиска
    search_fields = ('payment_user_trainer__user__user__username', 'payment_user_ward__user__username')
    # поля для фильтрации
    list_filter = ('payment_currency', 'payment_trainer_success', 'payment_ward_success')

    def trainer_user_short(self, obj):
        return obj.payment_user_trainer.user.user.username

    def ward_user_short(self, obj):
        return obj.payment_user_ward.user.username

    # переименование полей для отображения
    trainer_user_short.short_description = 'Trainer name'
    ward_user_short.short_description = 'Ward name'


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedBodyParameter(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('user_short', 'title_short', 'body_data', 'body_datetime')
    # поля для поиска
    search_fields = ('id', 'user__user__id', 'user__user__username', 'body_title')
    # поля для фильтрации
    list_filter = ('body_datetime',)

    def user_short(self, obj):
        return obj.user.user.username

    user_short.short_description = 'User name'


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedTargetBodyParameter(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('user_short', 'title_short', 'target_body_data', 'target_body_datetime')
    # поля для поиска
    search_fields = ('id', 'user__user__id', 'user__user__username', 'target_body_title')
    # поля для фильтрации
    list_filter = ('target_body_datetime',)

    def user_short(self, obj):
        return obj.user.user.username

    user_short.short_description = 'User name'


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedChat(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('users_list', 'chat_alive')
    # поля для фильтрации
    list_filter = ('chat_alive',)


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedChatMessage(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('user_short', 'short_message', 'message_chat', 'message_file')
    # поля для поиска
    search_fields = ('message_text', 'user__user__username')
    # поля для фильтрации
    list_filter = ('message_chat__chat_alive', 'message_datetime', 'message_readed')

    def user_short(self, obj):
        return obj.user.user.username

    user_short.short_description = 'Message author'


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedFeedback(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('target_user_short', 'author_user_short', 'short_title', 'short_text', 'feedback_rate')
    # поля для поиска
    search_fields = ('target_user__user__username', 'author_user__user__username', 'feedback_title', 'feedback_text')
    # поля для фильтрации
    list_filter = ('feedback_datetime', 'feedback_rate')

    def target_user_short(self, obj):
        return obj.target_user.user.username

    def author_user_short(self, obj):
        return obj.author_user.user.username

    target_user_short.short_description = 'Feedback target'
    author_user_short.short_description = 'Feedback author'


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedDefExerciseType(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('short_title', 'short_description')
    # поля для поиска
    search_fields = ('type_title', 'type_description')


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedDefTypesBundle(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('short_type', 'get_bundled_types')
    # поля для поиска
    search_fields = ('bundle_type__type_title', 'bundle_type__type_description')


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedDefExercise(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('short_title', 'short_description', 'exercise_type')
    # поля для поиска
    search_fields = ('exercise_type__type_title', 'exercise_type__type_description', 'exercise_title', 'exercise_description')


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedExerciseType(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('user_short', 'short_title', 'short_description', 'type_datetime')
    # поля для поиска
    search_fields = ('type_owner__user__username', 'type_title', 'type_description')
    # поля для фильтрации
    list_filter = ('type_datetime',)

    def user_short(self, obj):
        return obj.type_owner.user.username

    user_short.short_description = 'User owner'


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedTypesBundle(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('short_type', 'get_bundled_types',)
    # поля для поиска
    search_fields = ('bundle_type__type_title', 'bundle_type__type_description')
    # поля для фильтрации
    list_filter = ('bundle_datetime',)


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedExercise(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('user_short', 'exercise_type', 'short_title', 'short_description')
    # поля для поиска
    search_fields = ('exercise_owner__user__username', 'exercise_title', 'exercise_description',
                     'exercise_type__type_title', 'exercise_type__type_description')
    # поля для фильтрации
    list_filter = ('exercise_datetime',)

    def user_short(self, obj):
        return obj.exercise_owner.user.username

    user_short.short_description = 'User owner'


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedExerciseSet(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('user_short', 'short_title', 'short_description', 'get_set_exercises', 'get_set_def_exercises')
    # поля для поиска
    search_fields = ('set_owner__user__username', 'set_title', 'set_description')
    # поля для фильтрации
    list_filter = ('set_datetime',)

    def user_short(self, obj):
        return obj.set_owner.user.username

    user_short.short_description = 'User owner'


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedSharedExercise(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('shared_exercise_short', 'shared_rate', 'shared_copies', 'shared_datetime')
    # поля для поиска
    search_fields = ('shared_exercise__exercise_title', 'shared_exercise__exercise_description')
    # поля для фильтрации
    list_filter = ('shared_datetime',)

    def shared_exercise_short(self, obj):
        return obj.shared_exercise.short_title()

    shared_exercise_short.short_description = 'Shared exercise'


#  класс для кастомизации модели FitnessTrainer (раширения модели пользователя под тренера)
class ExtendedSharedSet(admin.ModelAdmin):
    # поля, отображаемые в модели
    list_display = ('shared_set_short', 'shared_rate', 'shared_copies', 'shared_datetime')
    # поля для поиска
    search_fields = ('shared_set__set_title', 'shared_set__set_description')
    # поля для фильтрации
    list_filter = ('shared_datetime',)

    def shared_set_short(self, obj):
        return obj.shared_set.short_title()

    shared_set_short.short_description = 'Shared set'


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

admin.site.register(Chat, ExtendedChat)
admin.site.register(ChatMessage, ExtendedChatMessage)

admin.site.register(Feedback, ExtendedFeedback)

admin.site.register(DefExerciseType, ExtendedDefExerciseType)
admin.site.register(DefTypesBundle, ExtendedDefTypesBundle)
admin.site.register(DefExercise, ExtendedDefExercise)

admin.site.register(ExerciseType, ExtendedExerciseType)
admin.site.register(TypesBundle, ExtendedTypesBundle)
admin.site.register(Exercise, ExtendedExercise)

admin.site.register(ExerciseSet, ExtendedExerciseSet)

admin.site.register(SharedExercise, ExtendedSharedExercise)
admin.site.register(SharedSet, ExtendedSharedSet)
