from dataclasses import field
from django import forms
from django.forms import ModelForm, ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder':'Brand Name or Username',
                'style':'border-radius:5px; border-color:grey'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter a valid email address',
                'style':'border-radius: 5px; border-color: grey',
            }),
        }
    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("An user with this email already exists!")
        return email
    def clean_username(self):
        return self.cleaned_data['username'].lower()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder':'Password must be 8-20 characters long', 'style':'border-radius: 5px; border-color: grey'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder':'Confirm your Password','style':'border-radius: 5px; border-color: grey'})
