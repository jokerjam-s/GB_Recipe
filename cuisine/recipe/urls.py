from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.start),
    path("index/", views.index, name="index"),
    path("", include("django.contrib.auth.urls")),
    path("register/", views.Register.as_view(), name="register"),
]