# Generated by Django 5.0.3 on 2024-04-04 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mrdg', '0003_alter_manseryuk_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manseryuk',
            name='day',
            field=models.IntegerField(default=4),
        ),
    ]