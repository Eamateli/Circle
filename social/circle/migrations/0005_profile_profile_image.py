# Generated by Django 5.0.2 on 2024-03-03 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('circle', '0004_alter_noise_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]