# Generated by Django 2.0.5 on 2018-06-18 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FitnessPersonalArea', '0002_auto_20180618_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setting',
            name='setting_title',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='trainingcontract',
            name='contract_end_datetime',
            field=models.DateTimeField(null=True),
        ),
    ]