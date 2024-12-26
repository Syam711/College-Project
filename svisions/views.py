from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .edsr_model import apply_super_resolution
import os

def upload_image(request):
    try:
        if request.method == "POST" and request.FILES.get("image"):
            # Get scale from user input
            scale = int(request.POST.get("scale", 2))  # Default to 2x

            # Save the uploaded file
            uploaded_file = request.FILES["image"]
            fs = FileSystemStorage()
            input_path = fs.save(uploaded_file.name, uploaded_file)
            input_path = fs.path(input_path)

            # Define output path
            output_filename = f"sr_{scale}x_{uploaded_file.name}"
            output_path = os.path.join(fs.location, output_filename)

            # Apply super-resolution using the new model
            sr_image_path = apply_super_resolution(input_path, output_path, scale)

            return render(request, "svisions/success.html", {
                "sr_image_url": fs.url(output_filename),
                "original_image_url": fs.url(uploaded_file.name),
                "scale": scale,
            })

        return render(request, "svisions/upload.html")

    except Exception as e:
        error_message = f"Error: {str(e)}"
        return render(request, "svisions/error.html", {"error_message": error_message})
