# Generated by Django 2.0.5 on 2018-07-15 18:00

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FitnessPersonalArea', '0004_auto_20180715_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traingym',
            name='gym_geo',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, geography=True, null=True, srid=4326),
        ),
    ]
