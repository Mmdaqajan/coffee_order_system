from django.urls import path

from .views import barista_dashboard


urlpatterns = [
    path("", barista_dashboard, name="barista-dashboard"),
]