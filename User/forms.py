from django.contrib.auth.forms import UserCreationForm
from django import forms
from User.models import Profile, User,Blogs
from django.contrib.auth.models import User


class registerForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=('image_field','consultant','about_me')
        widgets={
            'image_field': forms.FileInput(attrs={'class':'form-control textinput'}),
            'consultant':forms.CheckboxInput(attrs={'class':'form-check-input','onClick':'show()'}),
            'about_me':forms.Textarea(attrs={'class':'form-control textarea','rows':'4'}),
        }


class userForm(UserCreationForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class':'form-control textinput', 'type':'password', 'align':'center',}),
    )

    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={'class':'form-control textinput', 'type':'password', 'align':'center',}),
    )

    class Meta:
        model=User
        # forms.EmailField(, required=False)
        fields=('username','email')
        widgets={
            'username': forms.TextInput(attrs={'class':'form-control textinput','autocomplete':'off'}),
            'email': forms.TextInput(attrs={'class':'form-control textinput','type':'email',}),
        }


class CreateBlogs(forms.ModelForm):
    
    class Meta:
        model = Blogs
        fields = ("title","blogs")
        widgets = {
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        }