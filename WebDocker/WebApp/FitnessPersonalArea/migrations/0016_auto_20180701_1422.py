# Generated by Django 2.0.5 on 2018-07-01 14:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FitnessPersonalArea', '0015_auto_20180630_1042'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefExercise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exercise_title', models.CharField(max_length=100)),
                ('exercise_description', models.TextField(max_length=5000)),
                ('exercise_approaches', models.IntegerField(default=0)),
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
                ('bundle_subtypes', models.ManyToManyField(blank=True, null=True, related_name='bundled_subtypes', to='FitnessPersonalArea.DefExerciseType')),
                ('bundle_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bundled_type', to='FitnessPersonalArea.DefExerciseType')),
            ],
        ),
        migrations.AddField(
            model_name='defexercise',
            name='exercise_type',
            field=models.ManyToManyField(blank=True, null=True, to='FitnessPersonalArea.DefExerciseType'),
        ),
    ]
