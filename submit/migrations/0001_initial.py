# Generated by Django 5.0.3 on 2024-04-11 13:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Submit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('jm', '신생아작명'), ('gm', '개명신청'), ('sj', '사주상담'), ('etc', '기타')], max_length=20)),
                ('name', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('visit', models.CharField(blank=True, choices=[('visit', '방문상담'), ('call', '전화상담')], max_length=20)),
                ('wantdate', models.CharField(blank=True, max_length=30)),
                ('dad_name', models.CharField(blank=True, max_length=25)),
                ('mom_name', models.CharField(blank=True, max_length=25)),
                ('first_name_ch', models.CharField(blank=True, max_length=25)),
                ('first_name_kr', models.CharField(blank=True, max_length=25)),
                ('first_name_bon', models.CharField(blank=True, max_length=25)),
                ('dolrim', models.CharField(blank=True, max_length=25)),
                ('fav_name', models.CharField(blank=True, max_length=100)),
                ('avoid_name', models.CharField(blank=True, max_length=100)),
                ('adress', models.CharField(blank=True, max_length=100)),
                ('phone', models.CharField(max_length=20)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('description', models.TextField(blank=True)),
                ('process', models.CharField(choices=[('1', '입금대기'), ('2', '진행중'), ('3', '완료')], default='1', max_length=20, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50)),
                ('gen', models.CharField(max_length=1)),
                ('sl', models.CharField(max_length=10)),
                ('year', models.CharField(max_length=4)),
                ('month', models.CharField(max_length=2)),
                ('day', models.CharField(max_length=2)),
                ('hour', models.CharField(max_length=2)),
                ('min', models.CharField(max_length=2)),
                ('submit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='persons', to='submit.submit')),
            ],
        ),
    ]
