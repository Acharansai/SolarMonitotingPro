from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import context
from monitoring.models import SensorData
import json


@login_required
def home(request):

    latest = SensorData.objects.order_by("-timestamp").first()

    if latest:
        context = {
            "voltage": latest.voltage,
            "current": latest.current,
            "power": latest.power,
            "temperature": latest.temperature,
            "irradiance": getattr(latest, "irradiance", 0),
            "created_at": latest.timestamp,
        }
    else:
        context = {
            "voltage": 0,
            "current": 0,
            "power": 0,
            "temperature": 0,
            "irradiance": 0,
            "created_at": None,
        }

    readings = SensorData.objects.order_by("-timestamp")[:20]
    readings = list(readings)[::-1]

    labels = [reading.timestamp.strftime("%H:%M:%S") for reading in readings]

    power_values = [float(reading.power) for reading in readings]
    temperature_values = [float(reading.temperature) for reading in readings]
    voltage_values = [float(reading.voltage) for reading in readings]
    current_values = [float(reading.current) for reading in readings]

    context["labels"] = json.dumps(labels)
    context["power_values"] = json.dumps(power_values)
    context["temperature_values"] = json.dumps(temperature_values)
    context["voltage_values"] = json.dumps(voltage_values)
    context["current_values"] = json.dumps(current_values)

    return render(request, "dashboard/dashboard.html", context)