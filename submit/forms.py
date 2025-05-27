from django.forms import ModelForm, TextInput, EmailInput
from django import forms
import datetime
from .models import Submit, Person
import re

class NameSubmitForm(ModelForm):

    field_order = ['process', 'name', 'phone', 'visit', 'wantdate', 'email', 'adress', 'first_name_ch', 
                   'first_name_kr', 'first_name_bon', 'fav_name', 'avoid_name',
                   'dad_name', 'mom_name', 'dolrim', 'description']

    class Meta:
        model = Submit
        exclude = ['category', 'user']
        
        widgets = {
            'name': TextInput(attrs={'placeholder': '예) 김민수'}),
            'phone': TextInput(attrs={'placeholder': '예) 01012345678'}),
            'email': EmailInput(attrs={'placeholder': '예) email@gmail.com'}),
            'address': TextInput(attrs={'placeholder': '주소입력'}),
            'first_name_ch': TextInput(attrs={'placeholder': '예) 金'}),
            'first_name_kr': TextInput(attrs={'placeholder': '예) 김'}),
            'first_name_bon': TextInput(attrs={'placeholder': '예) 김해김'}),
            'fav_name': TextInput(attrs={'placeholder': '예) 철수,영수'}),
            'avoid_name': TextInput(attrs={'placeholder': '예) 광수,정수'}),
            'dad_name': TextInput(attrs={'placeholder': "아버지성함"}),
            'mom_name': TextInput(attrs={'placeholder': "어머니성함"}),
            'dolrim': TextInput(attrs={'placeholder': '필요한경우기재'}),
            'wantdate': TextInput(attrs={'placeholder': '예) 24.05.05'}),
        }
        
    def clean_phone(self): # NameSubmitForm과 동일한 로직
        phone_number = self.cleaned_data.get('phone')
        if phone_number:
            if re.search(r'[- ]', phone_number):
                raise forms.ValidationError("전화번호에는 하이픈(-)이나 공백을 포함할 수 없습니다.")
            if not phone_number.isdigit():
                raise forms.ValidationError("전화번호는 숫자만 입력해야 합니다. (하이픈, 공백 제외)")
        return phone_number

class SajuSubmitForm(ModelForm):

    field_order = ['process', 'name', 'phone', 'visit', 'wantdate', 'email', 'adress', 'description']

    class Meta:
        model = Submit
        exclude = ['category', 'user']
        widgets = {
            'name': TextInput(attrs={'placeholder': '예) 김민수'}),
            'phone': TextInput(attrs={'placeholder': '예) 01012345678'}),
            'email': EmailInput(attrs={'placeholder': '예) email@gmail.com'}),
            'wantdate': TextInput(attrs={'placeholder': '예) 24.05.05'}),
        }

    def __init__(self, *args, **kwargs):
        super(SajuSubmitForm, self).__init__(*args, **kwargs)
        # 원하는 선택지만 포함시키기
        self.fields['visit'].choices = [("call", "전화상담"),("visit", "방문상담")]
        
    def clean_phone(self): 
        phone_number = self.cleaned_data.get('phone')
        if phone_number:
            if re.search(r'[- ]', phone_number):
                raise forms.ValidationError("전화번호에는 하이픈(-)이나 공백을 포함할 수 없습니다.")
            if not phone_number.isdigit():
                raise forms.ValidationError("전화번호는 숫자만 입력해야 합니다. (하이픈, 공백 제외)")
        return phone_number
    


class EtcSubmitForm(ModelForm):

    field_order = ['process', 'name', 'phone', 'visit', 'wantdate', 'email', 'adress', 'description']

    class Meta:
        model = Submit
        exclude = ['category', 'user']
        widgets = {
            'name': TextInput(attrs={'placeholder': '예) 김민수'}),
            'phone': TextInput(attrs={'placeholder': '예) 01012345678'}),
            'email': EmailInput(attrs={'placeholder': '예) email@gmail.com'}),
            'wantdate': TextInput(attrs={'placeholder': '예) 24.05.05'}),
        }
    def __init__(self, *args, **kwargs):
        super(EtcSubmitForm, self).__init__(*args, **kwargs)
        # 원하는 선택지만 포함시키기
        self.fields['visit'].choices = [("call", "전화상담"),("visit", "방문상담")]
        
    def clean_phone(self): 
        phone_number = self.cleaned_data.get('phone')
        if phone_number:
            if re.search(r'[- ]', phone_number):
                raise forms.ValidationError("전화번호에는 하이픈(-)이나 공백을 포함할 수 없습니다.")
            if not phone_number.isdigit():
                raise forms.ValidationError("전화번호는 숫자만 입력해야 합니다. (하이픈, 공백 제외)")
        return phone_number

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
        exclude = ['submit', 'name', 'data']
