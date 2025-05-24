# from django.forms import ModelForm
# from .models import Manseryuk
# from django import forms
# import datetime


# class ManseryukForm(ModelForm):
#     today = datetime.date.today()
#     MONTH_CHOICES = []
#     for r in range(1, 13):
#         MONTH_CHOICES.append((r, r))
#     month = forms.ChoiceField(widget=forms.Select, choices=MONTH_CHOICES,
#                               initial=today.month, label="태어난 월(月) ")
#     DAY_CHOICES = []
#     for r in range(1, 32):
#         DAY_CHOICES.append((r, r))

#     day = forms.ChoiceField(widget=forms.Select, choices=DAY_CHOICES,
#                             initial=today.day, label="태어난 일(日) ")
    
#     field_order = ['name', 'sl', 'yd', 'gen', 'year', 'month', 'day', 'hour', 'min']

#     class Meta:
#         model = Manseryuk
#         fields = '__all__'

#         labels = {
#             "name": "이름 ",
#             "year": "년(年) ",
#             "month": "월(月) ",
#             "day": "일(日) ",
#             "yd": "평달/윤달 ",
#             "hour": "시간 ",
#             "min": "분 ",
#             "gen": "성별 ",
#             "sl": "음력/양력"
#         }