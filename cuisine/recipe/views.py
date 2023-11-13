from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
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


def recipe_add(request):
    """
    Добавление рецепта.
    :param request:
    :return:
    """
    if request.method == "POST":
        form = forms.RecipeAdd(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            ingredients = form.cleaned_data['ingredients']
            steps = form.cleaned_data['steps']
            time_cook = form.cleaned_data['time_cook']
            photo = form.cleaned_data['photo']
    else:
        form = forms.RecipeAdd()

    return render(request, 'recipe_add.html', {'form': form})


@login_required
def recipes(request):
    return render(request, 'recipes.html')


class Register(FormView):
    form_class = forms.UserCreateForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('register_ok')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
