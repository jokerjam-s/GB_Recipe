from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from . import forms
from . import models


# Create your views here.
def index(request):
    return render(request, "index.html")


def start(request):
    response = redirect('index/')
    return response


@login_required
def profile(request):
    return render(request, 'profile.html')


def register_ok(request):
    return render(request, 'registration/register_ok.html')


@login_required
def recipe_add(request):
    """
    Добавление рецепта.
    :param request:
    :return:
    """
    if request.method == "POST":
        form = forms.RecipeAdd(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['photo']
            file = FileSystemStorage()
            file_name = file.get_available_name(image.name) if file.exists(image.name) else image.name
            file.save(file_name, image)

            categories = form.cleaned_data['categories']
            recipe = models.Recipe(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                ingredients=form.cleaned_data['ingredients'],
                steps=form.cleaned_data['steps'],
                time_cook=form.cleaned_data['time_cook'],
                photo=file_name,
                user=request.user
            )

            recipe.save()
            for category in categories:
                category.recipes.add(recipe)
                category.save()

            return redirect(to='recipes')
    else:
        form = forms.RecipeAdd()

    return render(request, 'recipe_add.html', {'form': form})


@login_required
def recipes(request):
    recipes = models.Recipe.objects.filter(user=request.user)
    # todo: Вывод списка пользовательских рецептов, добавить пагинацию

    return render(request, 'recipes.html')


class Register(FormView):
    form_class = forms.UserCreateForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('register_ok')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
