from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from . import models


class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = models.User
        fields = UserCreationForm.Meta.fields + ("email", )


class RecipeAdd(forms.Form):
    """
    Добавление рецепта.
    """
    title = forms.CharField(max_length=150)
    description = forms.CharField(required=False)
    ingredients = forms.CharField(required=False)
    steps = forms.CharField(max_length=500)
    time_cook = forms.IntegerField(min_value=1)
    photo = forms.ImageField()