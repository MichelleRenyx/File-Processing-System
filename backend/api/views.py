from rest_framework import views, status
from rest_framework.response import Response
from .models import Document
from .serializers import DocumentSerializer
from rest_framework.permissions import AllowAny
import pandas as pd
from io import StringIO
from io import BytesIO
import spacy
from django.http import HttpResponse
import tempfile
import os

nlp = spacy.load('en_core_web_sm')

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
        

class ProcessDataView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Extract data from request
        pattern_description = request.data.get('patternDescription')
        file_data = request.data.get('fileData')

        if not pattern_description or not file_data:
            return Response({'error': 'Missing pattern description or file data'}, status=status.HTTP_400_BAD_REQUEST)

        # Convert file data from HTML back to DataFrame
        try:
            df = pd.read_html(StringIO(file_data))[0]
        except Exception as e:
            return Response({'error': f'Error processing HTML data: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        # Analyze the description to extract patterns and intended replacements
        doc = nlp(pattern_description)
        # Example: find patterns such as 'email', 'name', etc., and determine actions like 'redact', 'replace'
        patterns = [token.lemma_ for token in doc if token.pos_ in ['NOUN', 'PROPN']]
        actions = [token.lemma_ for token in doc if token.pos_ == 'VERB']
        # Simplistic NLP logic to determine regex pattern and replacement
        regex_patterns = { 'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7}\b', 'name': r'\b[A-Za-z]+\b' }
        replacements = { 'redact': 'REDACTED', 'replace': 'REPLACED' }

        regex_pattern = regex_patterns.get(patterns[0], '')
        replacement = replacements.get(actions[0], '')

        # Convert the string data back to DataFrame
        # html_data = StringIO(file_data)
        # df = pd.read_html(html_data)[0]

        # Apply regex to the DataFrame if applicable
        if regex_pattern and replacement:
            df.replace(regex_pattern, replacement, regex=True, inplace=True)

        # Convert modified DataFrame back to HTML
        updated_html = df.to_html(classes='table table-bordered')

        # Temporarily save data to file for download
        temp_dir = tempfile.mkdtemp()
        csv_file_path = os.path.join(temp_dir, "data.csv")
        excel_file_path = os.path.join(temp_dir, "data.xlsx")
        
        df.to_csv(csv_file_path, index=False)
        df.to_excel(excel_file_path, index=False, engine='openpyxl')
        
        return Response({'html_data': updated_html, 'csv_file_path': csv_file_path, 'excel_file_path': excel_file_path}, status=status.HTTP_200_OK)
    
class DownloadProcessedData(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request, file_path):
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                file_type = 'text/csv' if file_path.endswith('.csv') else 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                response = HttpResponse(f.read(), content_type=file_type)
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
                return response
        else:
            return Response({'error': 'File not found'}, status=status.HTTP_404_NOT_FOUND)

        
# class DownloadProcessedData(views.APIView):
#     permission_classes = [AllowAny]

#     def get(self, request, format_type):
#         data = request.session.get('processed_data')
#         if not data:
#             return Response({'error': 'No processed data available'}, status=status.HTTP_404_NOT_FOUND)

#         df = pd.DataFrame(data)
#         if format_type == 'csv':
#             response = HttpResponse(content_type='text/csv')
#             response['Content-Disposition'] = 'attachment; filename="processed_data.csv"'
#             df.to_csv(path_or_buf=response, index=False)
#         elif format_type == 'xlsx':
#             response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
#             response['Content-Disposition'] = 'attachment; filename="processed_data.xlsx"'
#             with pd.ExcelWriter(response) as writer:
#                 df.to_excel(writer, index=False)

#         return response
    
#     def download_csv(request):
#     # This is a placeholder function, you need to adapt it to your actual data handling logic
#         data = Document.objects.all().to_dataframe()  # Assuming using Django Pandas for DataFrame
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="processed_data.csv"'
#         data.to_csv(path_or_buf=response, index=False)
#         return response



#     def download_excel(request):
#         data = Document.objects.all().to_dataframe()  # Assuming using Django Pandas for DataFrame
#         response = HttpResponse(content_type='application/vnd.ms-excel')
#         response['Content-Disposition'] = 'attachment; filename="processed_data.xlsx"'
#         data.to_excel(excel_writer=response, index=False)
#         return response