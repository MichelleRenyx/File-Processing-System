from django.shortcuts import render

# Create your views here.
import pandas as pd
from rest_framework import views, status
from rest_framework.response import Response
from .models import Document
from .serializers import DocumentSerializer

from rest_framework.permissions import AllowAny

class DocumentUploadView(views.APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = DocumentSerializer(data=request.data)
        
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['file']
            file_instance = serializer.save()
            
            # 确定文件类型
            if uploaded_file.name.endswith('.csv'):
                file_instance.file_type = 'csv'
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith('.xlsx'):
                file_instance.file_type = 'excel'
                df = pd.read_excel(uploaded_file)
            else:
                return Response({'error': 'Unsupported file format'}, status=status.HTTP_400_BAD_REQUEST)
            
            file_instance.save()
            # 处理数据，比如清洗、转换等
            processed_data = df.to_html(classes='table table-striped')  # 转换为 HTML 表格
            return Response({'file_id': file_instance.id, 'data': processed_data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)