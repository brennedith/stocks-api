from django.urls import path
from . import views

app_name = "plt"

urlpatterns = [
    path('health', views.health, name="health"),
]