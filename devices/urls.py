from django.urls import path

from . import views


app_name = "devices"


urlpatterns = [

    path(
        "",
        views.device_list,
        name="device_list"
    ),

    path(
        "add/",
        views.device_create,
        name="device_create"
    ),

    path(
        "<int:pk>/",
        views.device_detail,
        name="device_detail"
    ),

    path(
        "<int:pk>/edit/",
        views.device_update,
        name="device_update"
    ),

    path(
        "<int:pk>/delete/",
        views.device_delete,
        name="device_delete"
    ),

    path("plants/", views.plant_list, name="plant_list"),

    path(
        "plants/add/",
        views.plant_create,
        name="plant_create",
    ),

    path(
        "plants/<int:pk>/",
        views.plant_detail,
        name="plant_detail",
    ),

    path(
        "plants/<int:pk>/edit/",
        views.plant_update,
        name="plant_update",
    ),

    path(
        "plants/<int:pk>/delete/",
        views.plant_delete,
        name="plant_delete",
    ),
]