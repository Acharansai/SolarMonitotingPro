from django.contrib import admin

from .models import Device, SolarPlant


@admin.register(SolarPlant)
class SolarPlantAdmin(admin.ModelAdmin):
    list_display = (
        "plant_name",
        "location",
        "capacity_kw",
        "status",
    )


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = (
        "device_name",
        "device_type",
        "plant",
        "status",
    )

    list_filter = (
        "device_type",
        "status",
    )

    search_fields = (
        "device_name",
        "serial_number",
    )