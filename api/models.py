from django.db import models
import uuid

class Request(models.Model):
    request_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.request_id)

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name="products")
    product_name = models.CharField(max_length=255)
    input_image_urls = models.TextField()
    output_image_urls = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.product_name