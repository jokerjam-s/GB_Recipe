from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin

# Register your models here.

from . import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', )
    search_fields = ('username', 'name', 'email',)


@admin.register(models.Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = ('title', 'description', 'ingredients', 'user',)
    search_fields = ('title',)


@admin.register(models.Category)
class RecipeAdmin(ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
