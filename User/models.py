from email.policy import default
from re import I
from ckeditor.fields import RichTextField
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
import datetime
from django.utils import timezone

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='Profile', on_delete=models.CASCADE)
    image_field = models.ImageField(upload_to='Images')
    rating = models.FloatField(default=0.0)
    consultant=models.BooleanField(default=False)
    about_me=models.TextField(default="")

    # def __str__(self):
    #     return self.usd

class Consultant(models.Model):
    consultant_id = models.OneToOneField(Profile, related_name='Consultant', on_delete=models.CASCADE)
    consultant_name = models.CharField(max_length=30, validators=[MinLengthValidator(5)])
    consultant_rating = models.FloatField(default=0.0)
    

    def __str__(self):
        return self.consultant_name

class Subscribe(models.Model):
    reg_user = models.ForeignKey("Profile", on_delete=models.CASCADE)
    reg_consultant = models.ForeignKey("Consultant", on_delete=models.CASCADE)
    # date = models.DateField(default=datetime.date.today())
    # time = models.TimeField(default=timezone.now)
    datetime=models.DateTimeField(default=datetime.datetime.now)
    meet_id = models.CharField(max_length=50,default="https://meet.com", validators=[MinLengthValidator(10)])

    def __str__(self):
        return self.meet_id

class Blogs(models.Model):
    title=models.CharField(max_length=50)
    blogs=RichTextField(blank=True,null=True,verbose_name='')
    # blogs=models.TextField()
    date_posted=models.DateTimeField(default=timezone.now)
    author=models.ForeignKey(Consultant,related_name='blog',on_delete=models.CASCADE)
    upvotes=models.ManyToManyField(User,related_name="upv")
    # globalblog=models.BooleanField(default=False)
    # upvotes=models.ForeignKey(User, verbose_name='', on_delete=models.CASCADE,related_name='upv')

    def get_absolute_url(self):
        return reverse('main')
    
  
