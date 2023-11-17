from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.start),
    path("index/", views.index, name="index"),
    path("", include("django.contrib.auth.urls")),
    path("register/", views.Register.as_view(), name="register"),
    path("register_ok/", views.register_ok, name="register_ok"),
    path("profile/", views.profile, name="profile"),
    path("recipes/add/", views.recipe_add, name="recipe_add"),
    path("recipes/edit/<int:recipe_id>", views.recipe_edit, name="recipe_edit"),
    path("recipes/del/", views.recipe_del, name="recipe_del"),
    path("recipes/", views.recipes, name="recipes"),
    path("recipe_view/<int:recipe_id>", views.recipe_view, name="recipe_view"),
]