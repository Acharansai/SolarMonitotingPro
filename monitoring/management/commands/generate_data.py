import time

from django.core.management.base import BaseCommand

from devices.models import Device
from monitoring.models import SensorData
from monitoring.services import SolarDataService


class Command(BaseCommand):

    help = "Generate Live Solar Sensor Data"

    def handle(self, *args, **kwargs):

        self.stdout.write(
            self.style.SUCCESS("Solar Data Generator Started...")
        )

        while True:

            devices = Device.objects.filter(status="ONLINE")

            for device in devices:

                reading = SolarDataService.generate_reading()

                SensorData.objects.create(
                    device=device,
                    voltage=reading["voltage"],
                    current=reading["current"],
                    power=reading["power"],
                    energy=reading["energy"],
                    temperature=reading["temperature"],
                    frequency=reading["frequency"],
                    power_factor=reading["power_factor"],
                )

                self.stdout.write(
                    f"✔ {device.device_name} | Power: {reading['power']} kW | Temp: {reading['temperature']}°C"
                )

            time.sleep(5)