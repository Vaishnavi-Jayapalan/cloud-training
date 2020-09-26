from django.shortcuts import render
from asset.serializers import AssetSerializer
from asset.models import Asset
from asset.models import FileType
from api_base.views import ApiBase
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from django.http import request
import sys
from rest_framework.parsers import MultiPartParser 
from rest_framework.parsers import FormParser
import os 
from python_cloud_storage import settings
from django.core.files.storage import FileSystemStorage
from asset.models import MimeType
from google.cloud import storage

class AssetView(ApiBase):

    @classmethod
    def createAsset(self, request):
        try:
            data = {}
            fileType = FileType.objects.get(type = request.POST.get('fileType'))
            data['fileType'] = fileType.id
            serializer = AssetSerializer(data = data)
            if serializer.is_valid():
                validatedData = self.validateFile(self, data['fileType'], request.FILES.get('file'))
                if validatedData is not False:
                    return self.generateBadDataErrorResponse(self, validatedData)
                serializer.save()
                self.uploadFile(self, serializer.data['id'], request.FILES.get('file'))
                self.uploadInCloud(self, request.FILES.get('file'), serializer.data['id'])
                return self.generatePostSuccessResponse(self, serializer)
            return self.generateFormErrorResponse(self, serializer)
        except Exception as e:
            # return self.handleException(self, e)
            return JsonResponse(e, safe = False)  
            # return e
    
    @classmethod
    def getAsset(self, request, id):
        try:
            asset = Asset.objects.get(id = id)
            serializer = AssetSerializer(asset)
            return self.generateGetSuccessResponse(self, serializer)
        except Exception as e:
            # return self.handleException(self, e)
            return JsonResponse(e, safe = False)

    def uploadFile(self, id, file):
        asset = Asset.objects.get(id = id)
        asset.fileName = file.name
        asset.save()
        return self
        
    def validateFileType(typeId, file):
        fileTypeModel = FileType.objects.get(id = typeId)
        typeArea = MimeType.objects.filter(fileType__id = fileTypeModel.id)
        if typeArea.count() is 0:
            return True
        return False

    def validateFileSize(typeId, file):
        fileTypeModel = FileType.objects.get(id = typeId)
        if file.size >= (fileTypeModel.maxSize * 1000000):
            return True
        return False

    def validateFile(self, typeId, file):
        if self.validateFileType(typeId, file):
            errors = {
                'field' : 'file',
                'message' : ['Uploaded file doesnt match given type']
            }
            return errors
        elif self.validateFileSize(typeId, file):
            errors = {
                'field' : 'file',
                'message' : ['Uploaded file exceeds 10MB']
            }
            return errors
        return False   

    def uploadInCloud(self, file, destination):
        storageClient = storage.Client.from_service_account_json(settings.GOOGLE_APPLICATION_CREDENTIALS)
        bucket = storageClient.bucket(settings.BUCKET_NAME)
        if not bucket:
            bucket = storageClient.create_bucket(settings.BUCKET_NAME)
        blob = bucket.blob(os.path.join(str(destination), file.name))
        blob.upload_from_file(file)
        return self

    def getAssetCloud(id):
        storage_client = storage.Client.from_service_account_json(settings.GOOGLE_APPLICATION_CREDENTIALS)
        bucket = storage_client.bucket(settings.BUCKET_NAME)
        blob = bucket.blob(string(id))

        return blob


        




