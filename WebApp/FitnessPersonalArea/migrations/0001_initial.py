# Generated by Django 2.0.5 on 2018-07-17 10:49

import FitnessPersonalArea.models
from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BodyParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body_title', models.CharField(max_length=100)),
                ('body_data', models.FloatField()),
                ('body_datetime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_alive', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_text', models.TextField(max_length=1000)),
                ('message_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('message_readed', models.BooleanField(default=False)),
                ('message_file', models.FileField(blank=True, null=True, upload_to=FitnessPersonalArea.models.chat_directory_path)),
                ('message_chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.Chat')),
            ],
        ),
        migrations.CreateModel(
            name='DefExercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise_title', models.CharField(max_length=100)),
                ('exercise_description', models.TextField(max_length=5000)),
                ('exercise_approaches', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DefExerciseType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_title', models.CharField(max_length=100)),
                ('type_description', models.TextField(max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='DefTypesBundle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bundle_subtypes', models.ManyToManyField(blank=True, related_name='bundled_subtypes', to='FitnessPersonalArea.DefExerciseType')),
                ('bundle_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bundled_type', to='FitnessPersonalArea.DefExerciseType')),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise_title', models.CharField(max_length=100)),
                ('exercise_description', models.TextField(max_length=5000)),
                ('exercise_approaches', models.IntegerField(blank=True, default=0, null=True)),
                ('exercise_datetime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='ExerciseSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('set_title', models.CharField(max_length=100)),
                ('set_description', models.TextField(max_length=5000)),
                ('set_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('set_def_exercises', models.ManyToManyField(blank=True, to='FitnessPersonalArea.DefExercise')),
                ('set_exercises', models.ManyToManyField(blank=True, to='FitnessPersonalArea.Exercise')),
            ],
        ),
        migrations.CreateModel(
            name='ExerciseType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_title', models.CharField(max_length=100)),
                ('type_description', models.TextField(max_length=5000)),
                ('type_datetime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback_title', models.CharField(max_length=100)),
                ('feedback_text', models.TextField(max_length=4000)),
                ('feedback_rate', models.FloatField(default=0)),
                ('feedback_datetime', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='FitnessTrainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trainer_employment_status', models.BooleanField(default=False)),
                ('trainer_description', models.TextField(default='Description', max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='FitnessUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fitness_user_bdate', models.DateField(blank=True, null=True)),
                ('fitness_user_type', models.CharField(choices=[('TRN', 'Тренер'), ('WRD', 'Подопечный')], default='WRD', max_length=3, verbose_name='user type')),
                ('fitness_user_photo', models.ImageField(blank=True, default=None, height_field='image_height', null=True, upload_to=FitnessPersonalArea.models.profile_photo_path, verbose_name='account photo', width_field='image_width')),
                ('fitness_user_gender', models.CharField(choices=[('MAL', 'Мужчина'), ('FEM', 'Женщина'), ('SEC', 'Секрет')], default='MAL', max_length=3, verbose_name='user gender')),
                ('fitness_user_destination_city', models.CharField(blank=True, default='', max_length=50, null=True, verbose_name='destination city')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_account', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MedicalNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medical_note_title', models.CharField(max_length=100)),
                ('medical_note_text', models.TextField(max_length=4000)),
                ('medical_note_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('medical_note_show', models.BooleanField(default=True)),
                ('medical_note_tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.FitnessUser')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectionPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projection_view_type', models.CharField(choices=[('FRT', 'Передний вид'), ('SD1', 'Боковой вид №1'), ('SD2', 'Боковой вид №2'), ('BCK', 'Задний вид')], default='FRT', max_length=3, verbose_name='projection type')),
                ('projection_view_date', models.DateField(default=django.utils.timezone.now)),
                ('projection_view_photo', models.ImageField(default=None, height_field='image_height', upload_to=FitnessPersonalArea.models.projection_photo_path, verbose_name='account photo', width_field='image_width')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.FitnessUser')),
            ],
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setting_title', models.CharField(max_length=100, unique=True)),
                ('setting_description', models.TextField(max_length=1000)),
                ('setting_param', models.CharField(default='', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='SharedExercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shared_rate', models.FloatField(default=0)),
                ('shared_copies', models.IntegerField(default=0)),
                ('shared_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('shared_exercise', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.Exercise')),
            ],
        ),
        migrations.CreateModel(
            name='SharedSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shared_rate', models.FloatField(default=0)),
                ('shared_copies', models.IntegerField(default=0)),
                ('shared_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('shared_set', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.ExerciseSet')),
            ],
        ),
        migrations.CreateModel(
            name='TargetBodyParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_body_title', models.CharField(max_length=100)),
                ('target_body_data', models.FloatField()),
                ('target_body_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.FitnessUser')),
            ],
        ),
        migrations.CreateModel(
            name='TrainerDoc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_title', models.TextField(max_length=1000)),
                ('doc_file', models.FileField(upload_to=FitnessPersonalArea.models.trainer_docs_path)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.FitnessTrainer')),
            ],
        ),
        migrations.CreateModel(
            name='TrainerPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trainer_price_hour', models.FloatField()),
                ('trainer_price_comment', models.CharField(default='', max_length=100)),
                ('trainer_price_currency', models.CharField(max_length=20)),
                ('trainer_price_creating_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('trainer_price_bargaining', models.BooleanField(default=True)),
                ('trainer_price_actuality', models.BooleanField(default=True)),
                ('trainer_price_show', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.FitnessTrainer')),
            ],
        ),
        migrations.CreateModel(
            name='TrainGym',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gym_name', models.CharField(max_length=100)),
                ('gym_description', models.TextField(max_length=1000)),
                ('gym_destination', models.CharField(max_length=100)),
                ('gym_geo', django.contrib.gis.db.models.fields.PointField(blank=True, geography=True, null=True, srid=4326)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.FitnessUser')),
            ],
        ),
        migrations.CreateModel(
            name='TrainingContract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_trainer_start', models.BooleanField(default=False)),
                ('contract_ward_start', models.BooleanField(default=False)),
                ('contract_hour_price', models.FloatField(default=0)),
                ('contract_currency', models.CharField(max_length=20)),
                ('contract_trainer_end', models.BooleanField(default=False)),
                ('contract_ward_end', models.BooleanField(default=False)),
                ('contract_create_datetime', models.DateField(default=django.utils.timezone.now)),
                ('contract_expire_datetime', models.DateField()),
                ('contract_end_datetime', models.DateTimeField(blank=True, null=True)),
                ('contract_trainer_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.FitnessTrainer')),
                ('contract_ward_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.FitnessUser')),
            ],
        ),
        migrations.CreateModel(
            name='TrainingPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_training_time', models.TimeField()),
                ('payment_price_per_hour', models.FloatField()),
                ('payment_currency', models.CharField(max_length=20)),
                ('payment_create_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('payment_expire_datetime', models.DateTimeField()),
                ('payment_end_datetime', models.DateTimeField(blank=True, null=True)),
                ('payment_trainer_success', models.BooleanField(default=False)),
                ('payment_ward_success', models.BooleanField(default=False)),
                ('payment_contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.TrainingContract')),
            ],
        ),
        migrations.CreateModel(
            name='TrainingSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_date', models.DateField(default=django.utils.timezone.now)),
                ('schedule_train_end', models.TimeField(default=django.utils.timezone.now)),
                ('schedule_train_start', models.TimeField(default=django.utils.timezone.now)),
                ('schedule_train_type', models.CharField(max_length=100)),
                ('author_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_schedule_user', to='FitnessPersonalArea.FitnessUser')),
                ('schedule_exercise_set', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='FitnessPersonalArea.ExerciseSet')),
                ('schedule_gym', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule_gym', to='FitnessPersonalArea.TrainGym')),
                ('schedule_train_tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('target_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_schedule_user', to='FitnessPersonalArea.FitnessUser')),
            ],
        ),
        migrations.CreateModel(
            name='TypesBundle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bundle_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('bundle_subtypes', models.ManyToManyField(blank=True, related_name='bundled_subtypes', to='FitnessPersonalArea.ExerciseType')),
                ('bundle_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bundled_type', to='FitnessPersonalArea.ExerciseType')),
            ],
        ),
        migrations.CreateModel(
            name='UserDiary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diary_note_title', models.CharField(max_length=100)),
                ('diary_note_text', models.TextField(max_length=4000)),
                ('diary_note_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('diary_note_show', models.BooleanField(default=True)),
                ('diary_note_tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.FitnessUser')),
            ],
        ),
        migrations.CreateModel(
            name='UserSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setting_data', models.CharField(default='', max_length=100)),
                ('default_setting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.Setting')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.FitnessUser')),
            ],
        ),
        migrations.AddField(
            model_name='trainingpayment',
            name='payment_training_schedule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.TrainingSchedule'),
        ),
        migrations.AddField(
            model_name='trainingpayment',
            name='payment_user_trainer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.FitnessTrainer'),
        ),
        migrations.AddField(
            model_name='trainingpayment',
            name='payment_user_ward',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.FitnessUser'),
        ),
        migrations.AddField(
            model_name='fitnesstrainer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.FitnessUser'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='author_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_feedback_user', to='FitnessPersonalArea.FitnessUser'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='target_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_feedback_user', to='FitnessPersonalArea.FitnessUser'),
        ),
        migrations.AddField(
            model_name='exercisetype',
            name='type_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.FitnessUser'),
        ),
        migrations.AddField(
            model_name='exerciseset',
            name='set_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.FitnessUser'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='exercise_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.FitnessUser'),
        ),
        migrations.AddField(
            model_name='exercise',
            name='exercise_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='FitnessPersonalArea.ExerciseType'),
        ),
        migrations.AddField(
            model_name='defexercise',
            name='exercise_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='FitnessPersonalArea.DefExerciseType'),
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.FitnessUser'),
        ),
        migrations.AddField(
            model_name='chat',
            name='users',
            field=models.ManyToManyField(to='FitnessPersonalArea.FitnessUser'),
        ),
        migrations.AddField(
            model_name='bodyparameter',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.FitnessUser'),
        ),
    ]