from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    
    file_type = serializers.CharField(required=False)  

    class Meta:
        model = Document
        fields = ('file', 'file_type')