from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from devices.models import Device
from monitoring.models import SensorData


@login_required
def monitoring_dashboard(request):

    devices = Device.objects.select_related("plant").all()

    selected_device_id = request.GET.get("device")

    selected_device = None
    latest = None
    readings = []

    if selected_device_id:

        selected_device = get_object_or_404(
            Device,
            pk=selected_device_id
        )

        latest = (
            SensorData.objects
            .filter(device=selected_device)
            .order_by("-timestamp")
            .first()
        )

        readings = list(
            SensorData.objects
            .filter(device=selected_device)
            .order_by("-timestamp")[:20]
        )

        readings.reverse()

    context = {
        "devices": devices,
        "selected_device": selected_device,
        "latest": latest,
        "readings": readings,
    }

    return render(
        request,
        "monitoring/monitoring.html",
        context
    )


@login_required
def monitoring_live_data(request):

    device_id = request.GET.get("device")

    if not device_id:
        return JsonResponse({
            "error": "Device ID is required"
        }, status=400)

    latest = (
        SensorData.objects
        .filter(device_id=device_id)
        .order_by("-timestamp")
        .first()
    )

    if not latest:
        return JsonResponse({
            "error": "No data available"
        }, status=404)

    return JsonResponse({

        "voltage": float(latest.voltage),

        "current": float(latest.current),

        "power": float(latest.power),

        "energy": float(latest.energy),

        "temperature": float(latest.temperature),

        "frequency": float(latest.frequency),

        "power_factor": float(latest.power_factor),

        "timestamp": latest.timestamp.strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

    })