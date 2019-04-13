from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class ServiceHealth(APIView):
    
    def get(self, request):
        """
        Get service health
        """
        return Response(status=status.HTTP_200_OK)
