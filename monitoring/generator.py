import os
import sys
import django
import random
import time


# Add project root to Python path
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, BASE_DIR)


# Configure Django
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()


# Import Django models AFTER django.setup()
from devices.models import Device
from monitoring.models import SensorData


print("========================================")
print(" SolarMonitorPro Sensor Data Generator")
print("========================================")


# Get first available device
device = (
    Device.objects
    .select_related("plant")
    .first()
)


if not device:

    print("")
    print("ERROR: No device found.")
    print("")
    print("Please create:")
    print("Solar Plant")
    print("    ↓")
    print("Device")
    print("")

    sys.exit(1)


print("")
print("Plant :", device.plant.plant_name)
print("Device:", device.device_name)
print("Type  :", device.get_device_type_display())
print("")


# Starting energy
energy = 0.0


while True:

    # Generate realistic values

    voltage = round(
        random.uniform(220, 240),
        2
    )

    current = round(
        random.uniform(5, 15),
        2
    )

    power = round(
        voltage * current,
        2
    )

    temperature = round(
        random.uniform(25, 45),
        2
    )

    frequency = round(
        random.uniform(49.8, 50.2),
        2
    )

    power_factor = round(
        random.uniform(0.90, 0.99),
        2
    )


    # Energy calculation
    #
    # Power is W
    # Convert to kW
    # Generator interval = 5 seconds

    energy += (
        power / 1000
    ) * (
        5 / 3600
    )


    # Save SensorData

    data = SensorData.objects.create(

        device=device,

        voltage=voltage,

        current=current,

        power=power,

        energy=round(
            energy,
            3
        ),

        temperature=temperature,

        frequency=frequency,

        power_factor=power_factor,

    )


    print(
        f"{device.device_name} | "
        f"V={voltage} V | "
        f"I={current} A | "
        f"P={power} W | "
        f"T={temperature} °C | "
        f"F={frequency} Hz | "
        f"PF={power_factor} | "
        f"E={round(energy, 3)} kWh"
    )


    # Wait 5 seconds

    time.sleep(5)