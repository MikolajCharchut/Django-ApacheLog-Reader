from django import forms  
from django.forms import FileInput
from .models import Log


class LogForm(forms.ModelForm):
    class Meta:
        model = Log
        fields = ['file']
        widgets = {
            'file' : FileInput(attrs={
                'class' : "form-file",
                'placeholder' : "Pliczek"
            })
        }