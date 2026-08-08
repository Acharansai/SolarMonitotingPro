from django.db import models
from devices.models import Device


class Alert(models.Model):

    SEVERITY_CHOICES = [
        ("INFO", "Info"),
        ("WARNING", "Warning"),
        ("CRITICAL", "Critical"),
    ]

    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("ACKNOWLEDGED", "Acknowledged"),
        ("RESOLVED", "Resolved"),
    ]

    device = models.ForeignKey(
        Device,
        on_delete=models.CASCADE,
        related_name="alerts"
    )

    title = models.CharField(max_length=150)

    message = models.TextField()

    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        default="WARNING"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="OPEN"
    )

    # Actual value that triggered the alert
    actual_value = models.FloatField(
        null=True,
        blank=True
    )

    # Threshold value
    threshold_value = models.FloatField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    resolved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.device.device_name} - {self.title}"