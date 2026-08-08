from django.db import models

class LiveSolarData(models.Model):
    voltage = models.DecimalField(max_digits=5, decimal_places=2)
    current = models.DecimalField(max_digits=5, decimal_places=2)
    power = models.DecimalField(max_digits=8, decimal_places=2)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    irradiance = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.created_at} - {self.power} W"