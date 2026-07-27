import random


class SolarDataService:

    @staticmethod
    def generate_reading():

        return {
            "voltage": round(random.uniform(390, 420), 2),
            "current": round(random.uniform(8, 15), 2),
            "power": round(random.uniform(3, 6), 2),
            "energy": round(random.uniform(100, 500), 2),
            "temperature": round(random.uniform(25, 55), 2),
            "frequency": round(random.uniform(49.8, 50.2), 2),
            "power_factor": round(random.uniform(0.90, 1.00), 2),
        }