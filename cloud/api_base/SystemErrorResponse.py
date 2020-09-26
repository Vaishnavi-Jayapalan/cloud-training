from django.http.response import JsonResponse
from rest_framework import status

class SystemErrorResponse():
    def generateSystemErrorResponse():
        errors = {}
        data = []
        message = {}
        message['message'] = 'System Error'
        data.append(message)
        errors['errors'] = data
        return JsonResponse(errors, safe = False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)