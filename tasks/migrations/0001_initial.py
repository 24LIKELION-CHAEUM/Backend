# Generated by Django 5.0.7 on 2024-07-29 07:09

import tasks.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('MED', 'Medication'), ('MEAL', 'Meal'), ('TASK', 'Task')], max_length=4)),
                ('time', models.TimeField()),
                ('date', models.DateField(default=tasks.models.get_current_date)),
                ('repeat_days', models.JSONField(blank=True, default=dict, null=True)),
                ('is_completed', models.BooleanField(default=False)),
            ],
        ),
    ]
