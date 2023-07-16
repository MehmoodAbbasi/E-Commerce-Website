from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm, UsernameField , PasswordChangeForm, PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext,gettext_lazy as _
from django.forms import ModelForm
from .models import Image , Customer
from django.contrib.auth import password_validation

class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Enter Password Again',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(label='Enter your email',required=False,  widget=forms.EmailInput(attrs={'class':'form-control'}))
            
class Meta:
    model = User
    fields = ['username','email','password1','password2']
    lables = {'email':'Email'}
    widgets = {'UserName':forms.TextInput(attrs={'class':'form-control'})}
        

class Loginform(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))        
    password = forms.CharField(label=_("Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))        



class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=("old Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','autofocus':True,'class':'form-control'}))
    new_password1 = forms.CharField(label=("New Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','autofocus':True,'class':'form-control'}),help_text=password_validation.password_validators_help_text_html())  
    new_password2 = forms.CharField(label=("Confirm Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','autofocus':True,'class':'form-control'})),         


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"),max_length=255,widget=forms.EmailInput(attrs={'autocomplete':'email','class':'form-control'}))
    


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=("New Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','autofocus':True,'class':'form-control'}),help_text=password_validation.password_validators_help_text_html())  
    new_password2 = forms.CharField(label=("Confirm Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','autofocus':True,'class':'form-control'})),         



class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name','locality','city','state','zipcode']
        widgets = {'name':forms.TextInput(attrs={'class':'form-control'})}, 
        widgets = {'locality':forms.TextInput(attrs={'class':'form-control'})}, 
        widgets = {'city':forms.TextInput(attrs={'class':'form-control'})}, 
        widgets = {'state':forms.Select(attrs={'class':'form-control'})}, 
        widgets = {'zipcode':forms.NumberInput(attrs={'class':'form-control'})}