from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from dal import autocomplete
from django.urls import reverse


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    first_name = forms.CharField(required=True, label="First Name")
    last_name = forms.CharField(required=True, label="Last Name") 

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("This email already used")
        return data  


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name','members')
        widgets = {'members': autocomplete.ModelSelect2Multiple(url='user-autocomplete', attrs={'data-html': True})}


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['branch', 'enrollment_no', 'year']                  
		  
