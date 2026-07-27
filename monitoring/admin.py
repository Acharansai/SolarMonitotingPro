from django.contrib import admin
from .models import SensorData


@admin.register(SensorData)
class SensorDataAdmin(admin.ModelAdmin):

    list_display = (
        "device",
        "voltage",
        "current",
        "power",
        "temperature",
        "timestamp",
    )

    list_filter = (
        "device",
    )

    ordering = (
        "-timestamp",
    )