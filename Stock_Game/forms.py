from django import forms
from datetime import date,time
from .models import Room
class CreateForm(forms.ModelForm):
    class Meta:
        model=Room
        widgets = {
            'desc': forms.Textarea(
            attrs={'placeholder': 'Enter description here'}),
            'end_in' :forms.DateField(
                widget=forms.TextInput(
                    attrs={'type': 'date'}
    )
            ),
        }
        exclude=('reg_user',)