# Generated by Django 5.0.2 on 2024-03-05 21:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circle', '0005_profile_profile_image'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='noise',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='noise_like', to=settings.AUTH_USER_MODEL),
        ),
    ]
