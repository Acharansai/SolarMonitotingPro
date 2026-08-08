import os
import random
import time
from datetime import datetime

import django

from alerts.services import check_alerts
from devices.models import Device

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from monitoring.models import LiveSolarData

print("Solar Data Generator Started...")

device = Device.objects.first()

if not device:
    print("No device found. Please create a device first.")
    exit()


while True:
    data = LiveSolarData.objects.create(
        voltage=round(random.uniform(160, 270), 2),
        current=round(random.uniform(5, 15), 2),
        power=round(random.uniform(0, 3500), 2),
        temperature=round(random.uniform(25, 70), 2),
        irradiance=round(random.uniform(50, 1000), 2),
        created_at=datetime.now()
    )

    check_alerts(device, data)

    print("Inserted one record")

    time.sleep(5)