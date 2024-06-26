# Generated by Django 5.0.3 on 2024-04-11 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mrdg', '0006_alter_manseryuk_day'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manseryuk',
            name='time',
        ),
        migrations.AddField(
            model_name='manseryuk',
            name='hour',
            field=models.CharField(max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='manseryuk',
            name='min',
            field=models.CharField(max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='manseryuk',
            name='day',
            field=models.CharField(max_length=2),
        ),
        migrations.AlterField(
            model_name='manseryuk',
            name='month',
            field=models.CharField(max_length=2),
        ),
        migrations.AlterField(
            model_name='manseryuk',
            name='year',
            field=models.CharField(max_length=4),
        ),
    ]
