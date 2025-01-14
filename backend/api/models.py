from django.db import models

# Create your models here.

class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    processed = models.BooleanField(default=False)
    file_type = models.CharField(max_length=10)  # 'csv' or 'excel'