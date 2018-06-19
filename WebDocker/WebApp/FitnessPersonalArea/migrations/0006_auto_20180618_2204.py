# Generated by Django 2.0.5 on 2018-06-18 22:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('FitnessPersonalArea', '0005_auto_20180618_2200'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trainingcontract',
            old_name='contract_trainer_agreement',
            new_name='contract_trainer_start',
        ),
        migrations.RenameField(
            model_name='trainingcontract',
            old_name='contract_ward_agreement',
            new_name='contract_ward_start',
        ),
        migrations.AlterField(
            model_name='trainingpayment',
            name='payment_training_schedule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='FitnessPersonalArea.TrainingSchedule'),
        ),
    ]