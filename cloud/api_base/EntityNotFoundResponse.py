from django.http.response import JsonResponse
from rest_framework import status

class EntityNotFoundResponse():
    def generateEntityNotFound():
        errors = {}
        data = []
        message = {}
        message['message'] = 'Resource Not Found'
        data.append(message)
        errors['errors'] = data
        return JsonResponse(errors, safe = False, status = status.HTTP_400_BAD_REQUEST)