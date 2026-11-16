import hashlib
import hmac
import json
import os

from cryptography.fernet import Fernet
from dotenv import load_dotenv
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from self_profile.models import SelfProfile as SelfProfileModel

from .serializer import InventoryPayloadSerializer

load_dotenv()

cipher = Fernet(os.environ["SECRET_ENCRYPTION_KEY"])


class InventoryPosts(APIView):
    def post(self, request):
        decrypted_secret = cipher.decrypt(
            bytes(SelfProfileModel.objects.first().encrypted_secret)
        )
        request_tag = request.data.get("tag", "")
        raw_books = request.data.get("books")

        books_json = json.dumps(raw_books, sort_keys=True, separators=(",", ":"))

        tag = hmac.new(
            decrypted_secret, books_json.encode("utf-8"), hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(request_tag, tag):
            return Response(
                {"message": "invalid signature"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = InventoryPayloadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
