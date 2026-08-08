import os
import random
import sys
import time

import django


# --------------------------------------------------
# Add project root to Python path
# --------------------------------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, BASE_DIR)


# --------------------------------------------------
# Configure Django
# --------------------------------------------------

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings"
)

django.setup()


# --------------------------------------------------
# Import models AFTER django.setup()
# --------------------------------------------------

from devices.models import Device
from monitoring.models import SensorData


print("========================================")
print(" SolarMonitorPro Sensor Data Generator")
print("========================================")


# --------------------------------------------------
# Get all devices
# --------------------------------------------------

devices = list(
    Device.objects
    .select_related("plant")
    .all()
)


if not devices:

    print()
    print("ERROR: No devices found.")
    print()
    print("Please create:")
    print("Solar Plant")
    print("    ↓")
    print("Device")
    print()

    sys.exit(1)


# --------------------------------------------------
# Display devices
# --------------------------------------------------

print()
print(f"Devices found: {len(devices)}")
print()

for device in devices:

    print(
        f"{device.plant.plant_name} | "
        f"{device.device_name} | "
        f"{device.get_device_type_display()}"
    )

print()


# --------------------------------------------------
# Energy tracking
# --------------------------------------------------

energy = {
    device.id: 0.0
    for device in devices
}


# --------------------------------------------------
# Start generator
# --------------------------------------------------

print("Starting data generation...")
print("Generating data every 5 seconds.")
print("Press CTRL+C to stop.")
print()


try:

    while True:

        for device in devices:

            # --------------------------------------
            # Generate realistic values
            # --------------------------------------

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


            # --------------------------------------
            # Energy calculation
            # --------------------------------------

            energy[device.id] += (
                power / 1000
            ) * (
                5 / 3600
            )


            # --------------------------------------
            # Save SensorData
            # --------------------------------------

            SensorData.objects.create(

                device=device,

                voltage=voltage,

                current=current,

                power=power,

                energy=round(
                    energy[device.id],
                    3
                ),

                temperature=temperature,

                frequency=frequency,

                power_factor=power_factor,

            )


            # --------------------------------------
            # Display generated data
            # --------------------------------------

            print(
                f"{device.plant.plant_name} | "
                f"{device.device_name} | "
                f"V={voltage} V | "
                f"I={current} A | "
                f"P={power} W | "
                f"T={temperature} °C | "
                f"F={frequency} Hz | "
                f"PF={power_factor} | "
                f"E={round(energy[device.id], 3)} kWh"
            )


        print("-" * 90)

        # ------------------------------------------
        # Wait 5 seconds
        # ------------------------------------------

        time.sleep(5)


except KeyboardInterrupt:

    print()
    print("========================================")
    print(" Sensor Data Generator Stopped")
    print("========================================")