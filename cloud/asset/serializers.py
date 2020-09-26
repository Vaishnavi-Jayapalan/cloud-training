from rest_framework import serializers
from asset.models import Asset 
from google.cloud import storage
from python_cloud_storage import settings
import datetime

class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ('id', 'fileType', 'fileName')
        extra_kwargs = {
            'fileName': {'read_only': True},
        }

    def to_representation(self, instance):
        response = super().to_representation(instance)
        storage_client = storage.Client.from_service_account_json(settings.GOOGLE_APPLICATION_CREDENTIALS)
        bucket = storage_client.bucket(settings.BUCKET_NAME)
        if response['id'] is not None and response['fileName'] is not None:
            path = str(response['id'])+'/'+response['fileName']
            blob = bucket.blob(path)
            response['url'] = blob.generate_signed_url(
                version="v4",
                expiration=datetime.timedelta(minutes=15),
                method="GET",
            )
        return response


