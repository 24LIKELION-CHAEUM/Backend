# Generated by Django 5.0.7 on 2024-07-20 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_userprofile_senior_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='relationship',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]