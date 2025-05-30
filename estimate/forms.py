from django.forms import ModelForm
from django import forms
import datetime
from .models import Estimate, Comment

class EstimateForm(ModelForm):

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

    GEN_CHOICES = [("male", "남"), ("female", "여")]
    gen = forms.ChoiceField(widget=forms.Select,
                            choices=GEN_CHOICES, label="성 별 ")
    SL_CHOICES = [("solar", "양력"), ("lunar", "음력"), ("lunar_y", "음력윤달")]
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
        model = Estimate
        exclude = ['user','count','data','phone','description']

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "이름",
                }
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['user','post']
        fields = ['content']