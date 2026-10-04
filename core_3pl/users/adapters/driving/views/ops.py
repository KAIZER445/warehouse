from config.permission import IsOps
from rest_framework.response import Response
from rest_framework.views import APIView

from ....models import Ops
from ..serializers.ops import OpsGetSerializer


class ListOps(APIView):
    permission_classes = (IsOps,)

    def get(self, request):
        ops = Ops.objects.all()
        serializer = OpsGetSerializer(ops, many=True)
        return Response(serializer.data)