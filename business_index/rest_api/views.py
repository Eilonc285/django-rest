from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import Business
from .serializers import BusinessSerializer
from .easy_web_scraper import get_first_business_info


# Create your views here.

class BusinessView(APIView):
    def __init__(self, **kwargs):
        super().__init__()
        self.business_title = None
        self.business_id = None
        self.business = None
        self.serialized_business_objects = None
        self.final_response = status.HTTP_500_INTERNAL_SERVER_ERROR

    def get(self, request, *args, **kwargs):
        params = dict(request.query_params.items())
        if len(params) == 2:
            return self.create_response_for_request_of_single_business(params)
        elif len(params) == 0:
            return self.create_response_for_request_of_all_businesses(params)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)  # never reached

    def post(self, request, *args, **kwargs):
        serializer = BusinessSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def create_response_for_request_of_single_business(self, params):
        try:
            self.assign_id_and_title_params_to_instance_attributes(params)
            self.make_query_for_matching_business_object_from_db()
            self.serialize_queried_objects()
            self.final_response = Response(self.serialized_business_objects)
        except Exception as e:
            pass  # all exceptions set a proper final response before raising exception.
        return self.final_response

    def assign_id_and_title_params_to_instance_attributes(self, params):
        try:
            self.business_id = params['id']
            self.business_title = params['title']
        except KeyError as e:
            print(e)
            self.final_response = Response(status=status.HTTP_400_BAD_REQUEST)
            raise e

    def make_query_for_matching_business_object_from_db(self):
        try:
            self.business = Business.objects.get(id=self.business_id, title=self.business_title)
        except ValueError as e:
            print(e)
            self.final_response = Response(status=status.HTTP_400_BAD_REQUEST)
            raise e
        except Business.DoesNotExist as e:
            print(e)
            self.final_response = Response(status=status.HTTP_404_NOT_FOUND)
            raise e

    def serialize_queried_objects(self, many_objects=False):
        serializer = BusinessSerializer(self.business, many=many_objects)
        try:
            self.serialized_business_objects = serializer.data
        except Exception as e:
            print(e)
            print('Serializer may not be updated to model changes.')
            self.final_response = Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            raise e

    def create_response_for_request_of_all_businesses(self, params):
        try:
            self.business = Business.objects.all()
            self.serialize_queried_objects(many_objects=True)
            self.final_response = Response(self.serialized_business_objects)
        except Exception as e:
            pass
        return self.final_response


class WebScraperView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            business = get_first_business_info(request.data)
        except ValueError as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = BusinessSerializer(data=business)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_404_NOT_FOUND)
