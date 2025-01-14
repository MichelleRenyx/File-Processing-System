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
            uploaded_file = request.FILES.get('file')
            file_instance = serializer.save(file_type='')  # Save first, without specifying file_type

            # Automatically determine file_type based on file extension
            if uploaded_file.name.endswith('.csv'):
                file_instance.file_type = 'csv'
            elif uploaded_file.name.endswith('.xlsx'):
                file_instance.file_type = 'excel'
            else:
                return Response({'error': 'Unsupported file format'}, status=status.HTTP_400_BAD_REQUEST)
            
            file_instance.save()  # update file_instance
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
