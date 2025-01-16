from rest_framework import views, status
from rest_framework.response import Response
from .models import Document
from .serializers import DocumentSerializer
from rest_framework.permissions import AllowAny
import pandas as pd
from io import StringIO
from io import BytesIO
import spacy
from botocore.exceptions import ClientError
import os
import uuid
import boto3
from django.conf import settings

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

        # Apply regex to the DataFrame if applicable
        if regex_pattern and replacement:
            df.replace(regex_pattern, replacement, regex=True, inplace=True)

        # Convert modified DataFrame back to HTML
        updated_html = df.to_html(classes='table table-bordered')

        # Upload to S3
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        csv_buffer = BytesIO()
        df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)

        unique_id = str(uuid.uuid4())
        csv_key = f"{unique_id}.csv"
        s3_client.upload_fileobj(csv_buffer, settings.AWS_STORAGE_BUCKET_NAME, csv_key)

        # Generate presigned URL for download
        response_url = s3_client.generate_presigned_url('get_object', Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': csv_key}, ExpiresIn=3600)
        return Response({'html_data': updated_html, 'download_url': response_url}, status=status.HTTP_200_OK)
    
class DownloadProcessedData(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )

        # Generate presigned URL
        try:
            response = s3_client.generate_presigned_url('get_object',
                                                        Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                                                                'Key': id},
                                                        ExpiresIn=3600)  # URL expires in 1 hour
            return Response({'url': response}, status=status.HTTP_200_OK)
        except ClientError as e:
            return Response({'error': str(e)}, status=status.HTTP_404_NOT_FOUND)