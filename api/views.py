from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Request, Product
from .tasks import process_csv_task
import csv
from io import StringIO
import uuid


@csrf_exempt
def upload_csv(request):
    if request.method == 'POST':
        if not request.FILES.get('file'):
            return JsonResponse({"error": "No file uploaded."}, status=400)

        file = request.FILES['file']
        if not file.name.endswith('.csv'):
            return JsonResponse({"error": "Invalid file format. Please upload a CSV file."}, status=400)

        # Generate a unique request ID
        request_id = uuid.uuid4()

        # Save the request to the database
        db_request = Request(request_id=request_id, status="pending")
        db_request.save()

        # Process the CSV file asynchronously
        csv_data = file.read().decode('utf-8')
        process_csv_task.delay(str(request_id), csv_data)

        return JsonResponse({"request_id": str(request_id), "message": "CSV uploaded successfully. Processing started."})


def status(request, request_id):
    try:
        db_request = Request.objects.get(request_id=request_id)
        return JsonResponse({"request_id": str(request_id), "status": db_request.status})
    except Request.DoesNotExist:
        return JsonResponse({"error": "Request not found."}, status=404)
