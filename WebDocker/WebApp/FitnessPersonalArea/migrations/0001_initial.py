# Generated by Django 2.0.5 on 2018-06-18 19:20

from django.conf import settings
import django.contrib.postgres.fields.jsonb
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
            name='FitnessTrainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trainer_employment_status', models.BooleanField(default=False)),
                ('trainer_description', models.TextField(max_length=5000)),
            ],
        ),
        migrations.CreateModel(
            name='FitnessUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fitness_user_type', models.CharField(choices=[('TRN', 'Trainer'), ('USL', 'Usual')], default='USL', max_length=3, verbose_name='user type')),
                ('fitness_user_photo', models.ImageField(default=None, height_field='image_height', upload_to='profiles_photo/%Y/%m/%d/', verbose_name='account photo', width_field='image_width')),
                ('fitness_user_gender', models.CharField(choices=[('MAL', 'Male'), ('FEM', 'Female'), ('OTH', 'Other')], default='MAL', max_length=3, verbose_name='user gender')),
                ('fitness_user_destination_city', models.CharField(default='', max_length=50, verbose_name='destination city')),
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
                ('medical_note_tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.FitnessUser')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectionPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('projection_view_type', models.CharField(choices=[('FRT', 'Front'), ('SD1', 'Side first'), ('SD2', 'Side second'), ('BCK', 'Back')], default='FRT', max_length=3, verbose_name='projection type')),
                ('projection_view_date', models.DateField(default=django.utils.timezone.now)),
                ('projection_view_photo', models.ImageField(default=None, height_field='image_height', upload_to='projection_view_photo/%Y/%m/%d/', verbose_name='account photo', width_field='image_width')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.FitnessUser')),
            ],
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('setting_title', models.CharField(max_length=100)),
                ('setting_description', models.TextField(max_length=1000)),
                ('setting_param', models.CharField(default='', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='TargetBodyParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_body_data', models.FloatField()),
                ('target_body_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('target_body_title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.BodyParameter')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.FitnessUser')),
            ],
        ),
        migrations.CreateModel(
            name='TrainerDoc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc_title', models.TextField(max_length=1000)),
                ('doc_file', models.FileField(upload_to='trainer_docs/%Y/%m/%d/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.FitnessTrainer')),
            ],
        ),
        migrations.CreateModel(
            name='TrainerPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trainer_price_hour', models.FloatField()),
                ('trainer_price_currency', models.CharField(max_length=20)),
                ('trainer_price_creating_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('trainer_price_bargaining', models.BooleanField(default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.FitnessTrainer')),
            ],
        ),
        migrations.CreateModel(
            name='TrainGym',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gym_name', models.CharField(max_length=100)),
                ('gym_description', models.CharField(max_length=1000)),
                ('gym_destination', models.CharField(max_length=100)),
                ('gym_geolocation', django.contrib.postgres.fields.jsonb.JSONField(db_index=True, default={'latitude': 0.0, 'longitude': 0.0})),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.FitnessUser')),
            ],
        ),
        migrations.CreateModel(
            name='TrainingContract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_trainer_agreement', models.BooleanField(default=False)),
                ('contract_ward_agreement', models.BooleanField(default=False)),
                ('contract_hour_price', models.FloatField(default=0)),
                ('contract_currency', models.CharField(max_length=20)),
                ('contract_trainer_end', models.BooleanField(default=False)),
                ('contract_ward_end', models.BooleanField(default=False)),
                ('contract_create_datetime', models.DateTimeField(default=django.utils.timezone.now)),
                ('contract_expire_datetime', models.DateTimeField()),
                ('contract_end_datetime', models.DateTimeField()),
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
                ('payment_end_datetime', models.DateTimeField()),
                ('payment_trainer_success', models.BooleanField(default=False)),
                ('payment_target_success', models.BooleanField(default=False)),
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
                ('schedule_gym', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule_gym', to='FitnessPersonalArea.TrainGym')),
                ('schedule_train_tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
                ('target_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target_schedule_user', to='FitnessPersonalArea.FitnessUser')),
            ],
        ),
        migrations.CreateModel(
            name='UserDiary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('diary_note_title', models.CharField(max_length=100)),
                ('diary_note_text', models.TextField(max_length=4000)),
                ('diary_note_datetime', models.DateTimeField(default=django.utils.timezone.now)),
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
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.TrainingSchedule'),
        ),
        migrations.AddField(
            model_name='trainingpayment',
            name='payment_user_target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.FitnessUser'),
        ),
        migrations.AddField(
            model_name='trainingpayment',
            name='payment_user_trainer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.FitnessTrainer'),
        ),
        migrations.AddField(
            model_name='fitnesstrainer',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.FitnessUser'),
        ),
        migrations.AddField(
            model_name='bodyparameter',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.FitnessUser'),
        ),
    ]
