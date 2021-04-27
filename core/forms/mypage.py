from django import forms

from core.models import User


class AddressUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'postal_code', 'address', 'phone']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': '侍太郎'}),
            'email': forms.EmailInput(attrs={'placeholder': 'samurai@samurai.com'}),
            'postal_code': forms.TextInput(attrs={'placeholder': '150-0043'}),
            'address': forms.TextInput(attrs={'placeholder': '東京都渋谷区道玄坂２丁目１１−１'}),
            'phone': forms.TextInput(attrs={'placeholder': '03-5790-9039'}),
        }
