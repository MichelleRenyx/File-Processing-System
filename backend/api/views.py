from rest_framework import views, status
from rest_framework.response import Response
from .models import Document
from .serializers import DocumentSerializer
from rest_framework.permissions import AllowAny
import pandas as pd

class DocumentUploadView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_file = request.FILES.get('file')
            file_instance = serializer.save()  # Save the file instance

            # Automatically determine file_type based on file extension
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
                file_instance.file_type = 'csv'
            elif uploaded_file.name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
                file_instance.file_type = 'excel'
            else:
                return Response({'error': 'Unsupported file format'}, status=status.HTTP_400_BAD_REQUEST)

            file_instance.save()  # update file_instance

            # Convert DataFrame to HTML
            html_data = df.to_html(classes='table table-bordered')
            return Response({'data': html_data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)