from django.urls import path
from .views import upload_csv, status

urlpatterns = [
    path('upload/', upload_csv, name='upload_csv'),
    path('status/<uuid:request_id>/', status, name='status'),
]
