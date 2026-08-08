from django.urls import path

from . import views


app_name = "monitoring"


urlpatterns = [

    path(
        "",
        views.monitoring_dashboard,
        name="dashboard"
    ),

    path(
        "live-data/",
        views.monitoring_live_data,
        name="live_data"
    ),

]