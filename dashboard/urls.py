from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path('', views.home, name='home'),
    path("live-data/", views.live_data, name="live_data"),

]