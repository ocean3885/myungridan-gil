# Generated by Django 5.0.3 on 2024-04-21 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estimate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='estimate',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]