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
    recipes = random.choices(models.Recipe.objects.all(), k=6)
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
                category.recipes.add(recipe)
                category.save()

            return redirect(to='recipes')
    else:
        form = forms.RecipeAdd()

    return render(request, 'recipe_add.html', {'form': form})


@login_required
def recipe_edit(request, recipe_id=0):
    if request.method == 'POST':
        form = forms.RecipeEdit(request.POST, request.FILES)
        if form.is_valid():
            id = form.cleaned_data["id"]
            recipe = get_object_or_404(models.Recipe, pk=recipe_id)
            if recipe_id == id:
                image = form.cleaned_data['photo']
                file = FileSystemStorage()
                file_name = file.get_available_name(image.name) if file.exists(image.name) else image.name
                file.save(file_name, image)

                categories = form.cleaned_data['categories']
                recipe.title = form.cleaned_data['title']
                recipe.description = form.cleaned_data['description']
                recipe.ingredients = form.cleaned_data['ingredients']
                recipe.steps = form.cleaned_data['steps']
                recipe.time_cook = form.cleaned_data['time_cook']
                recipe.photo = file_name
                recipe.user = request.user

                models.Category.objects.filter(recipe__id=id).delete()
                recipe.save()
                for category in categories:
                    category.recipes.add(recipe)
                    category.save()

            return redirect(to='recipes')
    else:
        recipe = get_object_or_404(models.Recipe, pk=recipe_id)

        print(recipe)

        form = forms.RecipeEdit(instance=recipe)
        # form.id = recipe.pk
        # form.title = recipe.title
        # form.ingredients = recipe.ingredients
        # form.description = recipe.description
        # form.steps = recipe.steps
        # form.time_cook = recipe.time_cook
        # form.photo = recipe.photo
        # form.categories = models.Category.objects.filter(recipes__id=recipe_id)

        print(form.__dict__)

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
    categories = models.Category.objects.filter(recipes__id=recipe_id)
    return render(request, "recipe_view.html", {"recipe": recipe, 'categories': categories})


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
