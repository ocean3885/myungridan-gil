# Generated by Django 5.0.3 on 2025-05-25 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estimate', '0007_inmyunghanja'),
    ]

    operations = [
        migrations.AddField(
            model_name='estimate',
            name='name_hanja',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
