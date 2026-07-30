from django.shortcuts import render
from monitoring.models import LiveSolarData

def dashboard(request):
    latest = LiveSolarData.objects.order_by("-created_at").first()
    data = LiveSolarData.objects.order_by("-created_at")[:20]

    labels = [d.created_at.strftime("%H:%M:%S") for d in reversed(data)]
    power_values = [float(d.power) for d in reversed(data)]

    context = {
        "power": latest.power if latest else 0,
        "voltage": latest.voltage if latest else 0,
        "current": latest.current if latest else 0,
        "temperature": latest.temperature if latest else 0,
        "irradiance": latest.irradiance if latest else 0,
        "created_at": latest.created_at if latest else "",
        "labels": labels,
        "power_values": power_values,
    }

    return render(request, "dashboard.html", context)