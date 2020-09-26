from django.db import models
from asset.models import Asset

class Customer(models.Model):
    name = models.CharField(max_length = 150, db_column = 'name')
    createdAt = models.DateTimeField(db_column = 'created_at', auto_now_add = True)
    updatedAt = models.DateTimeField(db_column = 'updated_at', auto_now = True)
    asset = models.ForeignKey(
        Asset,
        db_column = 'asset_id',
        on_delete = models.CASCADE,
        related_name = 'assets'
    )
    class Meta:
        db_table = 'customer'