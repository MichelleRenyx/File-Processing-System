from django.urls import path
from .views import DocumentUploadView
from .views import ProcessDataView

urlpatterns = [
    path('upload/', DocumentUploadView.as_view(), name='document-upload'),
    path('process-data/', ProcessDataView.as_view(), name='process-data'),
]