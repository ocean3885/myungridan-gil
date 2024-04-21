from django.forms import ModelForm
from django import forms
import datetime
from .models import Submit, Person

class NameSubmitForm(ModelForm):

    field_order = ['process', 'name', 'phone', 'visit', 'wantdate', 'email', 'adress', 'first_name_ch', 
                   'first_name_kr', 'first_name_bon', 'fav_name', 'avoid_name',
                   'dad_name', 'mom_name', 'dolrim', 'description']

    class Meta:
        model = Submit
        exclude = ['category', 'user']

class SajuSubmitForm(ModelForm):

    field_order = ['process', 'name', 'phone', 'visit', 'wantdate', 'email', 'adress', 'description']

    class Meta:
        model = Submit
        exclude = ['category', 'user']


class EtcSubmitForm(ModelForm):

    field_order = ['process', 'name', 'phone', 'visit', 'wantdate', 'email', 'adress', 'description']

    class Meta:
        model = Submit
        exclude = ['category', 'user']


class PersonForm(ModelForm):

    today = datetime.date.today()
    YEAR_CHOICES = []
    for r in range(1940, (today.year+1)):
        YEAR_CHOICES.append((r, r))
    YEAR_CHOICES.reverse()
    year = forms.ChoiceField(widget=forms.Select, choices=YEAR_CHOICES,
                             initial=today.year, label="태어난 년(年) ", required=True)

    MONTH_CHOICES = []
    for r in range(1, 13):
        MONTH_CHOICES.append((r, r))
    month = forms.ChoiceField(widget=forms.Select, choices=MONTH_CHOICES,
                              initial=today.month, label="태어난 월(月) ")

    DAY_CHOICES = []
    for r in range(1, 32):
        DAY_CHOICES.append((r, r))

    day = forms.ChoiceField(widget=forms.Select, choices=DAY_CHOICES,
                            initial=today.day, label="태어난 일(日) ")

    GEN_CHOICES = [("남", "남"), ("여", "여")]
    gen = forms.ChoiceField(widget=forms.Select,
                            choices=GEN_CHOICES, label="성 별 ")
    SL_CHOICES = [("양력", "양력"), ("음력", "음력"), ("음력윤달", "음력윤달")]
    sl = forms.ChoiceField(widget=forms.Select,
                           choices=SL_CHOICES, label="양력/음력 ")
    
    HOUR_CHOICES = []
    for r in range(0, 24):
        HOUR_CHOICES.append((r, r))

    hour = forms.ChoiceField(widget=forms.Select, choices=HOUR_CHOICES,
                            label="시간")
    
    MIN_CHOICES = []
    for r in range(0,60):
        MIN_CHOICES.append((r, r))

    min = forms.ChoiceField(widget=forms.Select, choices=MIN_CHOICES,
                            label="분")
    

    class Meta:
        model = Person
        exclude = ['submit', 'name']
