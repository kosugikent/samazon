from django import forms
from django.contrib.auth import authenticate

from core.models import User


class RegisterForm(forms.ModelForm):
    password_confirmation = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': '侍太郎'}),
            'email': forms.EmailInput(attrs={'placeholder': 'samurai@samurai.com'}),
            'postal_code': forms.TextInput(attrs={'placeholder': '150-0043'}),
            'address': forms.TextInput(attrs={'placeholder': '東京都渋谷区道玄坂２丁目１１−１'}),
            'phone': forms.TextInput(attrs={'placeholder': '03-5790-9039'}),
            'password': forms.PasswordInput
        }

    def clean(self):
        # emailが重複しないことをチェックするためにTrueに設定
        self._validate_unique = True
        password = self.cleaned_data['password']
        password_confirmation = self.cleaned_data['password_confirmation']
        if password != password_confirmation:
            self.add_error('password', 'パスワードが一致しません')
        return self.cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # パスワードをハッシュ化する
        user.set_password(self.cleaned_data['password'])
        # ログインで使用するバックエンドのパス
        user.backend = 'core.backends.UserModelBackend'
        user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_cache = None

    def clean(self):
        self.user_cache = authenticate(**self.cleaned_data)
        if self.user_cache is None:
            raise forms.ValidationError('メールアドレスまたはパスワードに誤りがあります')
        if self.user_cache.deleted_at:
            raise forms.ValidationError('退会済みユーザーです')
        return self.cleaned_data

    def get_user(self):
        return self.user_cache
