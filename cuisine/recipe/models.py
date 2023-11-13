from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.
class User(AbstractUser):
    """
    Пользователь системы
    """
    ...


class Recipe(models.Model):
    """
    Рецепт.
    """
    title = models.CharField(max_length=150, null=False)
    description = models.TextField(null=True, default=None)
    ingredients = models.TextField(null=True, default=None)
    steps = models.CharField(max_length=500)
    time_cook = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    photo = models.ImageField(upload_to='media/', null=True, default=None)

    class Meta:
        ordering = ['title']
        indexes = [
            models.Index(fields=['title']),
        ]


class Category(models.Model):
    """
    Категория рецепта.
    """
    name = models.CharField(max_length=50)
    recipes = models.ManyToManyField(Recipe)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]