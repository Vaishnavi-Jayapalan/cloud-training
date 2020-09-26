from django.db import models

class FileType(models.Model):
    type = models.CharField(max_length = 150, db_column = 'type', unique = True)
    maxSize = models.IntegerField()
    class Meta:
        db_table = 'file_type'

class MimeType(models.Model):
    type = models.CharField(max_length = 150, db_column = 'type', unique = True)
    fileType = models.ForeignKey(
        FileType,
        db_column = 'file_type_id',
        on_delete = models.CASCADE,
        related_name = 'mimeFileTypes'
    )
    class Meta:
        db_table = 'mime_type'

class Asset(models.Model):
    fileType = models.ForeignKey(
        FileType,
        db_column = 'file_type_id',
        on_delete = models.CASCADE,
        related_name = 'fileTypes',
        null = True
    )
    fileName = models.CharField(max_length = 150, db_column = 'file_name', null = True)
    createdAt = models.DateTimeField(db_column = 'created_at', auto_now_add = True)
    updatedAt = models.DateTimeField(db_column = 'updated_at', auto_now = True)
    class Meta:
        db_table = 'asset'
