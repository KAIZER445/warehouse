import hashlib
import hmac
import json
import os

from cryptography.fernet import Fernet
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from self_profile.models import SelfProfile as SelfProfileModel

from .models import Inventory as InventoryModel
from .serializer import InventoryPayloadSerializer

load_dotenv()

cipher = Fernet(os.environ["SECRET_ENCRYPTION_KEY"])
decrypted_secret = cipher.decrypt(
    bytes(SelfProfileModel.objects.first().encrypted_secret)
)


@csrf_exempt
class InventoryPosts(APIView):
    def post(self, request):
        serializer = InventoryPayloadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request_tag = serializer.validated_data["tag"]
        books = serializer.validated_data["books"]

        books_json = json.dumps(books, sort_keys=True, separators=(",", ":"))

        tag = hmac.new(
            decrypted_secret, books_json.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        try:
            if request_tag == tag:
                InventoryModel.save(data=serializer.validated_data)
            else:
                return Response(
                    {"message": "something went wrong"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ValueError as e:
            return Response({"error": str(e)}, status=400)
