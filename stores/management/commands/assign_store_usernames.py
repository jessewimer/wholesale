from django.core.management.base import BaseCommand
from stores.models import Store

class Command(BaseCommand):
    help = 'Assign usernames to stores interactively (only for stores without username)'

    def handle(self, *args, **options):
        stores = Store.objects.filter(username__isnull=True) | Store.objects.filter(username__exact='')
        for store in stores:
            self.stdout.write(f"Store: {store.name}")
            username = input("Enter username for this store: ").strip()

            if not username:
                self.stdout.write("No username entered; skipping.\n")
                continue

            store.username = username
            store.save()
            self.stdout.write(self.style.SUCCESS(f"Saved username '{username}' for store '{store.name}'.\n"))
