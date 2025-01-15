from rest_framework import views, status
from rest_framework.response import Response
from .models import Document
from .serializers import DocumentSerializer
from rest_framework.permissions import AllowAny
import pandas as pd
from io import StringIO
import spacy

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
        html_data = StringIO(file_data)
        df = pd.read_html(html_data)[0]

        # Apply regex to the DataFrame if applicable
        if regex_pattern and replacement:
            df.replace(regex_pattern, replacement, regex=True, inplace=True)

        # Convert modified DataFrame back to HTML
        updated_html = df.to_html(classes='table table-bordered')
        return Response({'data': updated_html}, status=status.HTTP_200_OK)