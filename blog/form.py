from django import forms
from .models import Post, User, Comment 
from django.contrib.auth.forms import UserCreationForm


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('category','title','text','tag','author','image')
        

class SignUpForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ("first_name","last_name","username", "email","phone_no","city","country","password1","password2",)


class LogInForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ("username","password",)


class ProfileEditForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, required=False)
    password2 = forms.CharField(widget=forms.PasswordInput, required=False)    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_no','city','country','image',"password1","password2")
    

class CommentForm(forms.ModelForm):
    class Meta:
        model =Comment
        fields = ['content','email','name',]

       
