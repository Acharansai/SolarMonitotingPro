from monitoring.services import SolarDataService


def generate_sensor_data():
    return SolarDataService.generate_reading()