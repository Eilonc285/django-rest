import django.http
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Business
from .serializers import BusinessSerializer


# Create your views here.

class TestView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = BusinessSerializer(Business.objects.all(), many=True)
        business_id = self.request.query_params.get('id')
        business_title = self.request.query_params.get('title')
        if business_id is not None or business_title is not None:
            try:
                serializer = BusinessSerializer(Business.objects.get(id=business_id, title=business_title))
            except Business.DoesNotExist as e:
                print(e)
                return django.http.HttpResponse(status=404)
        else:
            serializer = BusinessSerializer(Business.objects.all(), many=True)
        try:
            return Response(serializer.data)
        except Exception as e:
            print(e)
            print('Serializer may not be updated to model changes.')
            return django.http.HttpResponse(status=500)

    def post(self, request, *args, **kwargs):
        serializer = BusinessSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
