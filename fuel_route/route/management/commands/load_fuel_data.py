import csv
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from route.models import FuelStation


class Command(BaseCommand):
    help = "Load fuel station data from CSV file"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting fuel data import...")

        file_path = os.path.join(
            settings.BASE_DIR,
            "route",
            "data",
            "fuel-prices-for-be-assessment.csv"
        )

        created_count = 0

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                FuelStation.objects.create(
                    name=row["Truckstop Name"],
                    address=row["Address"],
                    city=row["City"],
                    state=row["State"],
                    retail_price=float(row["Retail Price"]),
                )
                created_count += 1

        self.stdout.write(f"Imported {created_count} fuel stations successfully.")