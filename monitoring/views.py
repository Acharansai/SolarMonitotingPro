from django.shortcuts import render
from monitoring.models import LiveSolarData

def dashboard(request):
    data = LiveSolarData.objects.order_by("-created_at")[:20]

    return render(request, "dashboard.html", {
        "data": data
    })