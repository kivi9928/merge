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
    # username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    phone_no = forms.CharField(required=True)
    city = forms.CharField(max_length=20)
    country = forms.CharField(max_length=20)
    image = forms.ImageField()
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone_no','city','country','image')

       

class CommentForm(forms.ModelForm):
    class Meta:
        model =Comment
        fields = ['content','email','name',]

       
