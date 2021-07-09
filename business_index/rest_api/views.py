import django.http
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Business
from .serializers import BusinessSerializer


# Create your views here.

class BusinessView(APIView):
    def get(self, request, *args, **kwargs):
        params = dict(request.query_params.items())
        if len(params) == 2:
            try:
                business_id = params['id']
                business_title = params['title']
            except KeyError as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
            try:
                serializer = BusinessSerializer(Business.objects.get(id=business_id, title=business_title))
            except Business.DoesNotExist as e:
                print(e)
                return Response(status=status.HTTP_404_NOT_FOUND)
            except ValueError as e:
                print(e)
                return Response(status=status.HTTP_400_BAD_REQUEST)
        elif len(params) == 0:
            serializer = BusinessSerializer(Business.objects.all(), many=True)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            return Response(serializer.data)
        except Exception as e:
            print(e)
            print('Serializer may not be updated to model changes.')
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        serializer = BusinessSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
