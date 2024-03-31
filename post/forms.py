from django import forms
from .models import Post, Text, Image

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['user','title']

class TextForm(forms.ModelForm):
    class Meta:
        model = Text
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'cols': 40}),  # Textarea 크기 조정
        }

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={'accept': 'image/*'}),  # 이미지 파일만 선택 가능하도록 설정
        }