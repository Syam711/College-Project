from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .models import UploadedImage
from .edsr_model import apply_super_resolution
from .custom_resize import resize_image
import os
from datetime import datetime

def upload_image(request):
    try:
        if request.method == "POST" and request.FILES.get("image"):
            uploaded_file = request.FILES["image"]
            fs = FileSystemStorage()
            input_path = fs.save(uploaded_file.name, uploaded_file)
            input_path = fs.path(input_path)

            scale = request.POST.get("scale")
            output_filename = f"processed_{uploaded_file.name}"
            output_path = os.path.join(fs.location, output_filename)

            if scale == "custom":
                # Custom resizing
                width = int(request.POST.get("width", 0))
                height = int(request.POST.get("height", 0))
                if width > 0 and height > 0:
                    processed_image_path = resize_image(input_path, output_path, width, height)
                    scale_label = f"{width}x{height}"
                else:
                    return render(request, "svisions/error.html", {"error_message": "Invalid dimensions."})
            else:
                # Use EDSR for predefined scales
                scale = int(scale)  # Convert to integer
                processed_image_path = apply_super_resolution(input_path, output_path, scale)
                scale_label = f"{scale}x"

            # Save image details to database
            uploaded_image = UploadedImage.objects.create(
                image_name=uploaded_file.name,
                processed_image_name=output_filename
            )

            return render(request, "svisions/success.html", {
                "image_id": uploaded_image.image_id,
                "image_name": uploaded_image.image_name,
                "uploaded_at": uploaded_image.uploaded_at,
                "processed_at": uploaded_image.processed_at,
                "sr_image_url": fs.url(output_filename),
                "original_image_url": fs.url(uploaded_file.name),
                "scale": scale_label,
            })

        return render(request, "svisions/upload.html")

    except Exception as e:
        return render(request, "svisions/error.html", {"error_message": f"Error: {str(e)}"})
