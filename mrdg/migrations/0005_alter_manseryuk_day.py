# Generated by Django 5.0.3 on 2024-04-10 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mrdg', '0004_alter_manseryuk_day'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manseryuk',
            name='day',
            field=models.IntegerField(default=10),
        ),
    ]