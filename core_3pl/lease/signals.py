import hashlib
import hmac
import json
import os

import requests
from cryptography.fernet import Fernet
from django.dispatch import Signal, receiver
from dotenv import load_dotenv
from inventory.models import Inventory as InventoryModel
from users.models import Tenant as TenantModel

from lease.core.domain.entity import Lease

load_dotenv()

cipher = Fernet(os.environ["SECRET_ENCRYPTION_KEY"])

lease_activated = Signal()


@receiver(lease_activated)
def send_books_to_storefront(sender, lease: Lease, **kwargs):
    lease_id = lease.id
    tenant: TenantModel = TenantModel.objects.get(id=lease.tenant_id)
    rows = InventoryModel.objects.filter(lease_id=lease_id)
    books = []
    for row in rows:
        books.append(
            {
                "id": str(row.id),
                "lease_id": str(lease_id),
                "title": row.title,
                "author": row.author,
                "description": row.description,
                "format_type": row.format_type,
                "length": str(row.length),
                "width": str(row.width),
                "thickness": str(row.thickness),
                "unit_weight": str(row.unit_weight),
                "quantity": row.quantity,
                "unit_volume": str(row.unit_volume),
                "total_volume": str(row.total_volume),
                "total_weight": str(row.total_weight),
                "created_at": row.created_at.isoformat(),
                "updated_at": row.updated_at.isoformat(),
            }
        )


    decrypted_secret = cipher.decrypt(bytes(tenant.encrypted_secret))
    
    books_json = json.dumps(books, sort_keys=True, separators=(",", ":"))
    
    tag = hmac.new(decrypted_secret, books_json.encode("utf-8"), hashlib.sha256).hexdigest()
    
    payload = {
        "lease_id": str(lease_id),
        "books": books,
        "tag": tag,
    }
    
    url = "https://" + tenant.base_url + "/inventory/posts"
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        print("status code:", response.status_code)
        print("Response text:", response.text)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
