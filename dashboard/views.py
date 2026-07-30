from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from monitoring.models import LiveSolarData
import json
from django.http import JsonResponse


@login_required
def home(request):

    latest = LiveSolarData.objects.order_by("-created_at").first()

    if latest:
        context = {
            "voltage": latest.voltage,
            "current": latest.current,
            "power": latest.power,
            "temperature": latest.temperature,
            "irradiance": latest.irradiance,
            "created_at": latest.created_at,
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

    readings = LiveSolarData.objects.order_by("-created_at")[:20]
    readings = list(readings)[::-1]

    labels = [r.created_at.strftime("%H:%M:%S") for r in readings]

    power_values = [float(r.power) for r in readings]
    temperature_values = [float(r.temperature) for r in readings]
    voltage_values = [float(r.voltage) for r in readings]
    current_values = [float(r.current) for r in readings]

    context["labels"] = json.dumps(labels)
    context["power_values"] = json.dumps(power_values)
    context["temperature_values"] = json.dumps(temperature_values)
    context["voltage_values"] = json.dumps(voltage_values)
    context["current_values"] = json.dumps(current_values)

    return render(request, "dashboard/dashboard.html", context)

@login_required
def live_data(request):

    latest = LiveSolarData.objects.order_by("-created_at").first()

    if latest:
        return JsonResponse({
            "voltage": float(latest.voltage),
            "current": float(latest.current),
            "power": float(latest.power),
            "temperature": float(latest.temperature),
            "irradiance": float(latest.irradiance),
            "created_at": latest.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })

    return JsonResponse({})