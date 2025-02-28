 Image Processing System

This project is a system for processing image data from CSV files. It accepts a CSV file containing product names and input image URLs, compresses the images to 50% of their original quality, and stores the processed image data in a database. The system provides APIs for uploading CSV files and checking the status of processing requests.

---

## Table of Contents
1. [Features](#features)
2. [Tech Stack](#tech-stack)
3. [Setup Instructions](#setup-instructions)
4. [API Documentation](#api-documentation)
5. [Database Schema](#database-schema)
6. [Asynchronous Workers](#asynchronous-workers)
7. [Postman Collection](#postman-collection)
8. [Low-Level Design (LLD)](#low-level-design-lld)
9. [Contributing](#contributing)
10. [License](#license)

---

## Features
- **Upload API**: Accepts a CSV file and returns a unique `request_id`.
- **Status API**: Allows users to check the status of a processing request.
- **Image Compression**: Compresses images to 50% of their original quality.
- **Database Storage**: Stores product data and processing status.
- **Asynchronous Processing**: Uses Celery for background task processing.
- **Webhook Integration**: Triggers a webhook after processing is complete (bonus feature).

---

## Tech Stack
- **Backend Framework**: Django (Python)
- **Database**: PostgreSQL
- **Asynchronous Task Queue**: Celery
- **Message Broker**: Redis
- **Image Processing**: Pillow (Python Imaging Library)
- **API Testing**: Postman

---

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL
- Redis

### Steps
1. Clone the repository:

   git clone https://github.com/your-username/image-processing-system.git
   cd image-processing-system
Create a virtual environment and activate it:

python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Set up the database:

Create a PostgreSQL database named image_processing_db.

Update the database settings in image_processing_system/settings.py:


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'image_processing_db',
        'USER': 'your-username',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

Run migrations:
python manage.py migrate

Start the Django development server:
python manage.py runserver

Start the Celery worker:
celery -A image_processing_system worker --loglevel=info --pool=solo
Start Redis (if not already running):
redis-server

API Documentation
1. Upload API
Endpoint: POST /api/upload/

Description: Uploads a CSV file for processing.

Request:

Method: POST

Body: form-data

Key: file (Type: File)

Value: Upload a CSV file.

Response:

Success:

json

{
    "request_id": "123e4567-e89b-12d3-a456-426614174000",
    "message": "CSV uploaded successfully. Processing started."
}
Error:

json

{
    "error": "No file uploaded."
}
2. Status API
Endpoint: GET /api/status/<request_id>/

Description: Checks the status of a processing request.

Request:

Method: GET

URL Parameter: request_id (e.g., 123e4567-e89b-12d3-a456-426614174000)

Response:

Success:

json

{
    "request_id": "123e4567-e89b-12d3-a456-426614174000",
    "status": "completed"
}
Error:

json

{
    "error": "Request not found."
}
Database Schema
Tables
requests

request_id (Primary Key): Unique ID for each request.

status: Processing status (e.g., pending, completed).

created_at: Timestamp when the request was created.

updated_at: Timestamp when the request was last updated.

products

product_id (Primary Key): Unique ID for each product.

request_id (Foreign Key): Links to the requests table.

product_name: Name of the product.

input_image_urls: Comma-separated input image URLs.

output_image_urls: Comma-separated output image URLs.

Asynchronous Workers
Task: process_csv_task
Description: Processes a CSV file asynchronously.

Steps:

Parses the CSV file.

Downloads and compresses images to 50% quality.

Saves the compressed images to the storage/output_images/ folder.

Updates the database with product data and output image URLs.

Updates the request status to completed.

Postman Collection
A Postman collection is provided for testing the APIs. Import the postman_collection.json file into Postman.

Low-Level Design (LLD)
System Diagram

+-------------------+       +-------------------+       +-------------------+
|                   |       |                   |       |                   |
|   Upload API      | ----> |   Image Processing| ----> |   Database        |
|                   |       |   Service         |       |                   |
+-------------------+       +-------------------+       +-------------------+
        |                           |                           |
        |                           |                           |
        v                           v                           v
+-------------------+       +-------------------+       +-------------------+
|                   |       |                   |       |                   |
|   Status API      | <---- |   Webhook Service | <---- |   Async Workers   |
|                   |       |                   |       |                   |
+-------------------+       +-------------------+       +-------------------+
Component Descriptions
Upload API: Accepts CSV files and returns a unique request_id.

Image Processing Service: Compresses images to 50% quality.

Database: Stores product data and request status.

Status API: Allows users to check the processing status.

Webhook Service: Triggers a webhook after processing is complete.

Async Workers: Handles background tasks like image processing.

Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.

Create a new branch (git checkout -b feature/your-feature).

Commit your changes (git commit -m 'Add your feature').

Push to the branch (git push origin feature/your-feature).

Open a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.


