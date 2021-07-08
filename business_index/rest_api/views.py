from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Business
from .serializers import BusinessSerializer


class TestView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = BusinessSerializer(Business.objects.all(), many=True)
        return Response(serializer.data)
