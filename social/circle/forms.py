from django import forms
from .models import Noise

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
