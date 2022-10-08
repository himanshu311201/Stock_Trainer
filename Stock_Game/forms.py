from django import forms
from datetime import date,time
from .models import Room
class CreateForm(forms.ModelForm):
    class Meta:
        model=Room
        widgets = {
            'starts_in': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control time'}),
            'ends_in': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control time'}),
        }
        exclude=('reg_user',)