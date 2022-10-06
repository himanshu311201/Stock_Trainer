from django.contrib import admin

# Register your models here.
from .models import Profile, Consultant, Subscribe

# Register your models here.
admin.site.register(Profile)
admin.site.register(Consultant)
admin.site.register(Subscribe)

