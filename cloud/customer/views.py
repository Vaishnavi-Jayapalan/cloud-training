from django.shortcuts import render
from customer.serializers import CustomerSerializer
from customer.models import Customer
from api_base.views import ApiBase
from django.http.response import JsonResponse
from django.http import request
import sys
import os 
from python_cloud_storage import settings
from rest_framework.parsers import JSONParser

class CustomerView(ApiBase):

    @classmethod
    def createCustomer(self, request):
        try:
            data = JSONParser().parse(request)
            serializer = CustomerSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return self.generatePostSuccessResponse(self, serializer)
            return self.generateFormErrorResponse(self, serializer)
        except Exception as e:
            # return self.handleException(self, e)
            return JsonResponse(e, safe = False)  
            # return e

    @classmethod
    def listCustomer(self):
        try:
            customers = Customer.objects.all()
            return self.generateGetSuccessResponse(self, customers)
        except Exception as e:
            # return self.handleException(self, e)
            return JsonResponse(e, safe = False)  
            # return e   
        
    