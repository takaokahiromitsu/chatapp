from django import forms

from .models import User

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm  # AuthenticationForm を追加

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email",)

# AuthenticationForm（便利機能）にもう機能が入っているのでpassでいい
class LoginForm(AuthenticationForm):
    pass

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username",)
        labels = {"username": "新しいユーザー名"}
        help_texts = {"username": ""}

class EmailChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)
        labels = {"email": "新しいメールアドレス"}