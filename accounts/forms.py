from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
     # ここにカスタムフィールドを追加するか、既存のフィールドをオーバーライドします。
     username = forms.CharField(
         label="ユーザー名",
         widget=forms.TextInput(attrs={'class': 'custom-class', 'placeholder': 'Username'}))
         #add here
     password = forms.CharField(
         label="パスワード", #ここでラベルをカスタムしている
         widget=forms.PasswordInput(attrs={'class': 'custom-class', 'placeholder': 'Password'}))