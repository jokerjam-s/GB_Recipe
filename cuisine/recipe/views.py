import random

from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView

from . import forms
from . import models


# Create your views here.
def index(request):
    recipes = models.Recipe.objects.all()
    if len(recipes) > 0:
        recipes = random.choices(recipes, k=6)
    return render(request, "index.html", {'recipes': recipes})


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
                recipe.categories.add(category)
        return redirect(to='recipes')
    else:
        form = forms.RecipeAdd()

    return render(request, 'recipe_add.html', {'form': form})


@login_required
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(models.Recipe, pk=recipe_id)
    if request.method == 'POST':
        form = forms.RecipeEdit(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            recipe = form.save(commit=False)
            categories = form.cleaned_data['categories']
            recipe.categories.clear()
            for category in categories:
                recipe.categories.add(category)
            recipe.save()

        return redirect(to='recipes')
    else:
        form = forms.RecipeEdit(instance=recipe)

    return render(request, 'recipe_edit.html', {'form': form})


@login_required
def recipes(request):
    """
    Просмотр списка рецептов пользователя.
    :param request:
    :return:
    """
    recipes_list = models.Recipe.objects.filter(user=request.user)
    paginator = Paginator(recipes_list, 15)
    page = request.GET.get('page')
    try:
        recipes_on_page = paginator.page(page)
    except PageNotAnInteger:
        recipes_on_page = paginator.page(1)
    except EmptyPage:
        recipes_on_page = paginator.page(paginator.num_pages)

    return render(request, 'recipes.html', {'page': page, 'recipes': recipes_on_page})


# @login_required
def recipe_view(request, recipe_id):
    recipe = get_object_or_404(models.Recipe, pk=recipe_id)
    # recipe.categories.all()
    return render(request, "recipe_view.html", {"recipe": recipe})


@login_required
def recipe_del(request):
    """
    Удаление рецепта.
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = forms.RecipeDel(request.POST)
        if form.is_valid():
            recipe_id = form.cleaned_data['recipe_id']
            models.Recipe.objects.filter(pk=recipe_id).delete()

    return redirect(to='recipes')


class Register(FormView):
    form_class = forms.UserCreateForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('register_ok')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
