from django.shortcuts import render
from django.views import View
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
import sys
from api_base.PostResponse import PostResponse
from api_base.PutResponse import PutResponse
from api_base.GetResponse import GetResponse
from api_base.DeleteResponse import DeleteResponse
from api_base.BadDataErrorResponse import BadDataErrorResponse
from rest_framework.exceptions import ValidationError
from api_base.FormValidationErrorException import FormValidationErrorException
from django.core.exceptions import ObjectDoesNotExist
from api_base.EntityNotFoundResponse import EntityNotFoundResponse
from api_base.SystemErrorResponse import SystemErrorResponse
from api_base.response import Response

# Create your views here.
class ApiBase(APIView):

    def markAsDeleted(self, model):
        if model.status:
            model.status = 0
        model.save()
        return model
    
    def handleEntitySave(self, serializer):
        serializer.save()
        return serializer

    def handleEntityDelete(self, model):
        if model.status:
            model.status = 0
        model.save()
        return model

    def generatePostSuccessResponse(self, model):
        response = PostResponse(model.data)
        return response.formatResponse()

    def generatePutSuccessResponse(self, model):
        response = PutResponse(model.data)
        return response.formatResponse()

    def generateDeleteSuccessResponse(self):
        response = DeleteResponse()
        return response.formatResponse()

    def generateGetSuccessResponse(self, model):
        response = GetResponse(model.data)
        return response.formatResponse()

    def generateResponse(self, data):
        response = Response(data = data, statusCode = 200, errors = None )
        return response.formatResponse()

    def validateEntityAuthority(self, model, data):
        try:
            model.objects.get(id = data)
            return model
        except Exception as e:
            return e
        
    def handleFormSubmission(self, serializer, request_data):
        form_data = serializer(data = request_data)
        if form_data.is_valid():
            serializer.save()
            return form_data
        raise ValidationError    
            
    def generateFormErrorResponse(self, model):
        response = BadDataErrorResponse(
            errors = FormValidationErrorException.formErrorResponseFormat(model)
        )
        return response.formatResponse()
    
    def generateBadDataErrorResponse(self, error):
        response = BadDataErrorResponse(errors = error)
        return response.formatResponse()
        
    def handleException(self, e):
        if isinstance(e, ValidationError):
            response = BadDataErrorResponse(errors = e)
            return response.formatResponse()
        if isinstance(e, ObjectDoesNotExist):
            return EntityNotFoundResponse.generateEntityNotFound() 
        return SystemErrorResponse.generateSystemErrorResponse()    


