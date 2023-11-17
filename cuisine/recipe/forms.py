from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from . import models


class UserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = models.User
        fields = UserCreationForm.Meta.fields + ("email",)


class RecipeAdd(forms.Form):
    """
    Добавление рецепта.
    """
    categories_data = models.Category.objects.all()

    title = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control', }))
    description = forms.CharField(required=False,
                                  widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control', }))
    ingredients = forms.CharField(required=True,
                                  widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control', }))
    steps = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control', }))
    time_cook = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control', }))
    categories = forms.ModelMultipleChoiceField(queryset=categories_data, required=True, to_field_name="id",
                                                widget=forms.CheckboxSelectMultiple())
    photo = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}, ))


class RecipeEdit(forms.ModelForm):
    # id = forms.IntegerField(widget=forms.HiddenInput())
    # categories_data = models.Category.objects.all()
    #
    # title = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'class': 'form-control', }))
    # description = forms.CharField(required=False,
    #                               widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control', }))
    # ingredients = forms.CharField(required=True,
    #                               widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control', }))
    # steps = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control', }))
    # time_cook = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control', }))
    # categories = forms.ModelMultipleChoiceField(queryset=categories_data, required=True, to_field_name="id",
    #                                             widget=forms.CheckboxSelectMultiple())
    # photo = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}, ))

    class Meta:
        model = models.Recipe
        fields = ('title', 'description', 'ingredients', 'steps', 'time_cook', 'categories', 'photo',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', }),
            'description': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', }),
            'ingredients': forms.Textarea(attrs={'rows': 5, 'class': 'form-control', }),
            'steps': forms.Textarea(attrs={'rows': 5, 'class': 'form-control', }),
            'time_cook': forms.NumberInput(attrs={'class': 'form-control', }),
            'categories': forms.CheckboxSelectMultiple(),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}, )
        }


class RecipeDel(forms.Form):
    recipe_id = forms.IntegerField(widget=forms.HiddenInput())
