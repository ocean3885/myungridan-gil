# Generated by Django 5.0.3 on 2024-05-03 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_profile_add'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bgimg',
            field=models.ImageField(blank=True, default='default_bg.jpg', null=True, upload_to='profile_pics/'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(blank=True, default='default_user.png', null=True, upload_to='profile_pics/'),
        ),
    ]
