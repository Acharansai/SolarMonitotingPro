from monitoring.models import SensorData
from devices.models import Device


class DashboardService:

    @staticmethod
    def get_dashboard_summary():

        latest = SensorData.objects.order_by("-timestamp").first()

        total_devices = Device.objects.count()

        online_devices = Device.objects.filter(
            status="ONLINE"
        ).count()

        if latest:

            return {
                "power": latest.power,
                "temperature": latest.temperature,
                "voltage": latest.voltage,
                "energy": latest.energy,
                "online_devices": online_devices,
                "total_devices": total_devices,
            }

        return {
            "power": 0,
            "temperature": 0,
            "voltage": 0,
            "energy": 0,
            "online_devices": online_devices,
            "total_devices": total_devices,
        }