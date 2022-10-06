from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator

class Profile(models.Model):
    user = models.OneToOneField(User, related_name='Profile', on_delete=models.CASCADE)
    email_id = models.CharField(max_length=30, validators=[MinLengthValidator(5)])
    image_field = models.ImageField(upload_to='Images/', max_length=500)
    rating = models.FloatField()

    def __str__(self):
        return self.email_id

class Consultant(models.Model):
    consultant_id = models.OneToOneField(Profile, related_name='Consultant', on_delete=models.CASCADE)
    consultant_name = models.CharField(max_length=30, validators=[MinLengthValidator(5)])
    consultant_rating = models.FloatField()

    def __str__(self):
        return self.consultant_name

class Subscribe(models.Model):
    reg_user = models.ForeignKey("Profile", on_delete=models.CASCADE)
    reg_consultant = models.ForeignKey("Consultant", on_delete=models.CASCADE)
    date = models.DateField
    time = models.TimeField()
    meet_id = models.CharField(max_length=50, validators=[MinLengthValidator(10)])

    def __str__(self):
        return self.meet_id

