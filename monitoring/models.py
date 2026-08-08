from django.db import models

from devices.models import Device


class SensorData(models.Model):

    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name="sensor_data"
    )

    voltage = models.DecimalField(max_digits=8, decimal_places=2)

    current = models.DecimalField(max_digits=8, decimal_places=2)

    power = models.DecimalField(max_digits=10, decimal_places=2)

    energy = models.DecimalField(max_digits=10, decimal_places=2)

    temperature = models.DecimalField(max_digits=5, decimal_places=2)

    frequency = models.DecimalField(max_digits=5, decimal_places=2)

    power_factor = models.DecimalField(max_digits=4, decimal_places=2)

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.device.device_name} - {self.timestamp}"


class LiveSolarData(models.Model):
    voltage = models.DecimalField(max_digits=5, decimal_places=2)
    current = models.DecimalField(max_digits=5, decimal_places=2)
    power = models.DecimalField(max_digits=8, decimal_places=2)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    irradiance = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField()

    '''
    class Meta:
        managed = False
        db_table = "solar_data"
    '''