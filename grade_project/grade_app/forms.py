from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm 
from .models import Gradebook, Grade


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email',)

class GradebookCreationForm(ModelForm):
    class Meta:
        model = Gradebook
        fields = ['title',]