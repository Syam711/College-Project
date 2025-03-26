from django.db import models
from django.utils.timezone import now, localtime

class UploadedImage(models.Model):
    id = models.AutoField(primary_key=True)  # Ensures ID is always an integer
    image_name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(default=now)
    processed_at = models.DateTimeField(null=True, blank=True)  # Set manually after processing
    processed_image_name = models.CharField(max_length=255, blank=True, null=True)

    def formatted_uploaded_at(self):
        return localtime(self.uploaded_at).strftime("%Y:%m:%d %H:%M:%S")

    def formatted_processed_at(self):
        return localtime(self.processed_at).strftime("%Y:%m:%d %H:%M:%S") if self.processed_at else "Not Processed"

    def __str__(self):
        return f"Image {self.image_name} - Processed: {self.processed_image_name}"
