# Generated by Django 5.0.7 on 2024-07-26 15:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_alter_userprofile_profile_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Emotion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField()),
                ('emotion', models.CharField(choices=[('happy', '행복'), ('neutral', '평범'), ('sad', '슬픔'), ('angry', '분노')], max_length=10)),
                ('description', models.TextField(blank=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_emotions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
