from django.shortcuts import render
from openai import OpenAI
from rest_framework import views, status
from rest_framework.response import Response
from .models import Document
from .serializers import DocumentSerializer
from rest_framework.permissions import AllowAny
import pandas as pd
from io import StringIO
from io import BytesIO
from botocore.exceptions import ClientError
import os
import uuid
import boto3
from django.conf import settings

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", settings.OPENAI_API_KEY))

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
            html_data = df.to_html(classes='table table-bordered', index=False) # index=False to exclude row numbers
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

        # Call OpenAI API with HTML and natural language description
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an intelligent assistant. Please edit the HTML data based on the instructions provided and return only the modified HTML."},
                    {"role": "user", "content": f"Here is the HTML table: {file_data}"},
                    {"role": "user", "content": f"Instruction: {pattern_description} Edit this HTML as per these instructions and return only the HTML code without any additional text or comments."}
                ],
                model="gpt-4o-mini"  # use the gpt-4o-mini model
            )
            modified_html = chat_completion.choices[0].message.content.strip()
            
        except Exception as e:
            print("Error with OpenAI API: ", str(e))
            return Response({'error': f'Error with OpenAI API: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        # Convert modified HTML back to DataFrame
        try:
            modified_df = pd.read_html(StringIO(modified_html))[0]
        except Exception as e:
            print("Error processing modified HTML to DataFrame: ", str(e))
            return Response({'error': f'Error processing modified HTML to DataFrame: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Upload to S3
        s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME
        )
        csv_buffer = BytesIO()
        modified_df.to_csv(csv_buffer, index=False)
        csv_buffer.seek(0)

        unique_id = str(uuid.uuid4())
        csv_key = f"{unique_id}.csv"
        s3_client.upload_fileobj(csv_buffer, settings.AWS_STORAGE_BUCKET_NAME, csv_key)

        # Generate presigned URL for download
        response_url = s3_client.generate_presigned_url('get_object', Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': csv_key}, ExpiresIn=3600)
        return Response({'html_data': modified_html, 'download_url': response_url}, status=status.HTTP_200_OK)
    
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
        

def index(request):
    return render(request, 'index.html')