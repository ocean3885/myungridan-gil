# Generated by Django 5.0.3 on 2024-04-15 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submit', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submit',
            name='process',
            field=models.CharField(blank=True, choices=[('1', '입금대기'), ('2', '진행중'), ('3', '완료')], default='1', max_length=20),
        ),
    ]
