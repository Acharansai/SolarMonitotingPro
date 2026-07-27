from django.db import models


class SolarPlant(models.Model):
    STATUS_CHOICES = [
        ("ONLINE", "Online"),
        ("OFFLINE", "Offline"),
        ("MAINTENANCE", "Maintenance"),
    ]

    plant_name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    capacity_kw = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ONLINE",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["plant_name"]
        verbose_name = "Solar Plant"
        verbose_name_plural = "Solar Plants"

    def __str__(self):
        return self.plant_name

class Device(models.Model):

    DEVICE_TYPES = [
        ("INVERTER", "Inverter"),
        ("METER", "Energy Meter"),
        ("BATTERY", "Battery"),
        ("WEATHER", "Weather Station"),
        ("SENSOR", "Sensor"),
    ]

    STATUS_CHOICES = [
        ("ONLINE", "Online"),
        ("OFFLINE", "Offline"),
        ("MAINTENANCE", "Maintenance"),
    ]

    plant = models.ForeignKey(
        SolarPlant,
        on_delete=models.CASCADE,
        related_name="devices"
    )

    device_name = models.CharField(max_length=100)

    serial_number = models.CharField(
        max_length=100,
        unique=True
    )

    manufacturer = models.CharField(max_length=100)

    model = models.CharField(max_length=100)

    device_type = models.CharField(
        max_length=20,
        choices=DEVICE_TYPES
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ONLINE"
    )

    installed_on = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["device_name"]

    def __str__(self):
        return f"{self.device_name} ({self.plant.plant_name})"