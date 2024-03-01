from django import forms
from .models import Noise
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NoiseForm(forms.ModelForm):
    body = forms.CharField(required=True,
       widget=forms.widgets.Textarea(
           attrs={
               "placeholder": "Make your Noise!",
               "class": "form-control",
           }
       ),
       label="",  
    )
    
    class Meta:
        model = Noise
        exclude = ("user",)
        
class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="", max_length=100,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1','password2')
