from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from . import models


class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = models.User
        fields = UserCreationForm.Meta.fields + ("email", )
