from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from .models import Profile




class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model=User
        fields=('username',"email",'password1','password2')


class Update_profile(ModelForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())
    class Meta:
        model=User
        fields = ['username', 'email']

class Update_image(ModelForm):
    class Meta:
        model=Profile
        fields = ['image']
