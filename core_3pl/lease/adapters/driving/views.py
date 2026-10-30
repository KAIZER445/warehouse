from rest_framework.views import APIView
from config.permission import IsTenant
from lease.core.domain.ports_service import LeaseServicePort
from lease.core.application.services import LeaseService
from lease.adapters.driven.repository import LeaseRepository
from .serializers import CreateQuoteSerializer, QuoteResponseSerializer, ActivateLeaseSerializer, ActivateLeaseResponseSerializer
from lease.core.domain.book import Book
from rest_framework.response import Response

class CreateQuote(APIView):
    permission_classes = (IsTenant,)
    service: LeaseServicePort = LeaseService(LeaseRepository())

    def post(self, request):
        serializer = CreateQuoteSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        books = []
        for item in serializer.validated_data["books"]:
            book = Book(**item)
            books.append(book)

        tenant_id = request.user.tenant.id

        try:
            result = self.service.create_quote(books=books, tenant_id=tenant_id)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        return Response(QuoteResponseSerializer(result).data, status=201)

class ActivateLease(APIView):
    permission_classes = (IsTenant,)
    service: LeaseServicePort = LeaseService(LeaseRepository())

    def post(self, request, lease_id):
        serializer = ActivateLeaseSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        tenant_id = request.user.tenant.id

        try:
            result = self.service.activate_lease(
                lease_id=lease_id,
                tenant_id=tenant_id,
                selected_space=data["selected_space"],
                term_months=data["term_months"],
                start_date=data["start_date"],
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        return Response(ActivateLeaseResponseSerializer(result).data, status=200)