from django.dispatch import Signal, receiver

lease_activated = Signal()

@receiver(lease_activated)
def send_books_to_storefront(sender, **kwargs):
    print("fgfg")
