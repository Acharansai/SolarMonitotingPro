from django.urls import path

from . import views

app_name = "alerts"

urlpatterns = [
    path("", views.alert_list, name="alert_list"),
    path("export/excel/", views.export_alerts_excel, name="export_alerts_excel"),
    path("export/pdf/", views.export_alerts_pdf, name="export_alerts_pdf"),
]