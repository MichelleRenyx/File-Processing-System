from django.urls import path
from .views import DocumentUploadView
from .views import ProcessDataView
from .views import DownloadProcessedData

urlpatterns = [
    path('upload/', DocumentUploadView.as_view(), name='document-upload'),
    path('process-data/', ProcessDataView.as_view(), name='process-data'),
    # path('download/<str:id>/', DownloadProcessedData.as_view(), name='download-processed-data'),
]