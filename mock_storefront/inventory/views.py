from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response

@csrf_exempt
class inventoryPosts(APIView):

    def post():
        return Response("hello")
