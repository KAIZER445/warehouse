from decimal import Decimal
from django.core.management.base import BaseCommand
from capacity.models import Capacity

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("--total", type=Decimal, default=Decimal("10000000"))

    def handle(self, *args, **options):
        if Capacity.objects.exists():
            self.stdout.write("Capacity already exists, skipping.")
            return

        capacity = Capacity.objects.create(total_capacity=options["total"])
        self.stdout.write(self.style.SUCCESS(f"Created capacity: {capacity.id}"))