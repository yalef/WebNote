from django import forms

from django.contrib.auth.models import User
from .models import Post

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password','email')

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title','text')