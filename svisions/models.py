from django.db import models

class UploadedImage(models.Model):
    image_id = models.AutoField(primary_key=True)  # Explicit primary key
    image_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(auto_now=True)
    processed_image_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image {self.image_id} - {self.image_name} (Processed: {self.processed_image_name})"
