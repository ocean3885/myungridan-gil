from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['category','title','is_all','is_side','is_home','content','image']
