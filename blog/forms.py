from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from blog.models import Comment, Post
User = get_user_model()

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.widgets.Input(attrs={'class': 'form-control', 'placeholder': 'Your First Name'}))
    last_name = forms.CharField(widget=forms.widgets.Input(attrs={'class': 'form-control', 'placeholder': 'Your Last Name'}))
    username = UsernameField(widget=forms.widgets.Input(attrs={'class': 'form-control', 'placeholder': 'Enter Username'}))
    email = forms.EmailField(required=True, widget=forms.widgets.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password1 = forms.CharField(required=True, label='Password', widget=forms.widgets.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password', 'type': 'password'}))
    password2 = forms.CharField(required=True, label='Confirm Password', widget=forms.widgets.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'type': 'password'}))
    class Meta(UserCreationForm):
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter password',
            'type': 'password',
        }
    ))

class BlogForm(forms.ModelForm):

    title = forms.CharField(max_length=255, required=True, widget=forms.widgets.Input(
        attrs={'class': 'form-control', 'placeholder': 'Blog title'}))
    content = forms.CharField(required=True, widget=forms.widgets.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Blog content'}))
    # slug = forms.CharField(max_length=255, required=True, widget=forms.widgets.Input(
    #     attrs={'class': 'form-control', 'placeholder': 'Blog slug'}))

    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('author','slug',)


class CommentForm(forms.ModelForm):
    content = forms.CharField(required=True, label = 'Comment', widget=forms.widgets.Textarea(attrs={'class': 'form-control', 'placeholder': 'Type your comment here'}))
    class Meta:
        model = Comment
        fields = ('content',)