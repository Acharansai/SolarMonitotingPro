from alerts.models import Alert


def check_alerts(device, data):

    # Low Voltage
    if float(data.voltage) < 180:
        Alert.objects.create(
            device=device,
            title="Low Voltage",
            message=f"Voltage dropped to {data.voltage} V",
            severity="WARNING",
            actual_value=float(data.voltage),
            threshold_value=180,
        )

    # High Voltage
    elif float(data.voltage) > 260:
        Alert.objects.create(
            device=device,
            title="High Voltage",
            message=f"Voltage increased to {data.voltage} V",
            severity="WARNING",
            actual_value=float(data.voltage),
            threshold_value=260,
        )

    # High Temperature
    if float(data.temperature) > 60:
        Alert.objects.create(
            device=device,
            title="High Temperature",
            message=f"Temperature reached {data.temperature} °C",
            severity="CRITICAL",
            actual_value=float(data.temperature),
            threshold_value=60,
        )

    # Low Irradiance
    if float(data.irradiance) < 150:
        Alert.objects.create(
            device=device,
            title="Low Irradiance",
            message=f"Irradiance dropped to {data.irradiance}",
            severity="INFO",
            actual_value=float(data.irradiance),
            threshold_value=150,
        )

    # No Power Generation
    if float(data.power) == 0:
        Alert.objects.create(
            device=device,
            title="No Power Generation",
            message="Power generation is zero.",
            severity="CRITICAL",
            actual_value=float(data.power),
            threshold_value=0,
        )