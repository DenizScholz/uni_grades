from django.contrib import admin
from .models import Gradebook, Grade

# Register your models here.
admin.site.register(Gradebook)
admin.site.register(Grade)
