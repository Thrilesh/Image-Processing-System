from celery import shared_task
from .models import Request, Product
from .services.image_processing import process_images
import csv
from io import StringIO
import os


@shared_task
def process_csv_task(request_id, csv_data):
    # Parse the CSV data
    csv_file = StringIO(csv_data)
    reader = csv.DictReader(csv_file)

    output_rows = []
    for row in reader:
        product_name = row["Product Name"]
        input_urls = row["Input Image Urls"].split(",")

        # Process images
        output_urls = process_images(input_urls, "storage/output_images")

        # Save product data to the database
        db_request = Request.objects.get(request_id=request_id)
        Product.objects.create(
            request=db_request,
            product_name=product_name,
            input_image_urls=",".join(input_urls),
            output_image_urls=",".join(output_urls)
        )

        # Add row to output CSV
        output_rows.append({
            "Product Name": product_name,
            "Input Image Urls": ",".join(input_urls),
            "Output Image Urls": ",".join(output_urls)
        })

    # Generate output CSV
    output_csv_path = os.path.join("storage", "output.csv")
    with open(output_csv_path, mode="w", newline="") as file:
        writer = csv.DictWriter(
            file, fieldnames=["Product Name", "Input Image Urls", "Output Image Urls"])
        writer.writeheader()
        writer.writerows(output_rows)

    # Update request status
    db_request.status = "completed"
    db_request.save()
