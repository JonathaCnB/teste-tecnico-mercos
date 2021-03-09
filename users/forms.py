from django.contrib.auth import forms

from .models import User


# form personalizado para alteração de user
class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User


# form personalizado para criação de user
class UserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = User
