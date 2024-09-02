from django import forms

from django.contrib.auth.forms import UserChangeForm,PasswordChangeForm,UserCreationForm
from django.contrib.auth import password_validation
from django.contrib.auth.models import User


class Add_User_Form(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password (again)', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','password1','password2']
        lables = {'email':'Email'}
        widgets = {
            'email':forms.EmailInput(attrs={'class':'form-control','required':'required'}),
            'first_name':forms.TextInput(attrs={'class':'form-control','required':'required'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','required':'required'}),
            'username':forms.TextInput(attrs={'class':'form-control','required':'required'}),
            
            
        }