# Generated by Django 2.0.5 on 2018-10-01 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FitnessPersonalArea', '0004_bodyparameter_body_show'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectionphoto',
            name='projection_view_description',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
