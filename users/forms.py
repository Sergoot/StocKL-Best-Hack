from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.forms import TextInput, PasswordInput, NumberInput

from .models import CustomUser


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'id': 'exampleInputEmail1',
        'class': 'form-control',
        'placeholder': 'example@box.com',
    }
    ))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'type': 'password',
        'class': 'form-control',
        'id': 'exampleInputPassword1'
    }
    ))


class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'type': 'password',
        'class': 'form-control',
        'id': 'exampleInputPassword1'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'type': 'password',
        'class': 'form-control',
        'id': 'exampleInputPassword2'}))

    class Meta:
        model = CustomUser
        fields = ('email',)
        widgets = {'email': TextInput(
            attrs={
                'id':'exampleInputEmail1',
                'class': 'form-control',
            }),
            'password1': PasswordInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class ValueForm(forms.Form):
    value = forms.FloatField(widget=NumberInput(attrs={
        'id': 'InputValue',
        'class': 'form-control',
    }))


# class BuyForm(forms.Form):
#     value = forms.FloatField(widget=NumberInput())
#
# class SendForm(forms.Form):
#