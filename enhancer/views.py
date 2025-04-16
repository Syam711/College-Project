from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.utils.timezone import now, localtime
from django.http import JsonResponse
from .models import UploadedImage
from .custom_resize import resize_image
from .edsr_model import apply_super_resolution
from .post_processing import apply_post_processing  # Import post-processing module
import os
import cv2

def home_page(request):
    return render(request, "enhancer/home.html")
    
# Allowed image formats
ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp'}
MAX_FILE_SIZE_MB = 10  # Max allowed file size (in MB)
MAX_DIMENSION = 5000  # Maximum allowed width/height

def is_valid_image(file):
    # Check file extension
    ext = os.path.splitext(file.name)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, "Invalid file type! Only JPG, PNG, and BMP are allowed."

    # Check file size (convert bytes to MB)
    file_size_mb = file.size / (1024 * 1024)
    if file_size_mb > MAX_FILE_SIZE_MB:
        return False, "File size exceeds 10MB limit!"

    return True, None

def upload_image(request):
    try:
        if request.method == "POST" and request.FILES.get("image"):
            uploaded_file = request.FILES["image"]

            # Validate file type and size
            is_valid, error_message = is_valid_image(uploaded_file)
            if not is_valid:
                return render(request, "enhancer/error.html", {"error_message": error_message})

            fs = FileSystemStorage()
            input_path = fs.save(uploaded_file.name, uploaded_file)
            input_path = fs.path(input_path)

            scale = request.POST.get("scale")
            output_filename = f"processed_{uploaded_file.name}"
            output_path = os.path.join(fs.location, output_filename)

            # Save initial record in DB (before processing)
            uploaded_image = UploadedImage.objects.create(
                image_name=uploaded_file.name,
                uploaded_at=now(),  # Set upload time now
                processed_at=None  # Processing not done yet
            )

            # Process image based on the selected scale
            if scale == "custom":
                width = int(request.POST.get("width", 0))
                height = int(request.POST.get("height", 0))

                # Validate width and height
                if width <= 0 or height <= 0 or width > MAX_DIMENSION or height > MAX_DIMENSION:
                    return render(request, "enhancer/error.html", {"error_message": "Invalid image dimensions!"})

                processed_image_path = resize_image(input_path, output_path, width, height)
            else:
                scale = int(scale)  # Convert to integer
                processed_image_path = apply_super_resolution(input_path, output_path, scale)

                # Apply post-processing on the super-resolved image
                processed_image = cv2.imread(processed_image_path)
                enhanced_image = apply_post_processing(processed_image)

                # Save the final enhanced image
                cv2.imwrite(processed_image_path, enhanced_image)

            # Update record with processed image details
            uploaded_image.processed_image_name = output_filename
            uploaded_image.processed_at = now()  # Set processing time
            uploaded_image.save()

            # Convert to local time and format it
            formatted_uploaded_at = localtime(uploaded_image.uploaded_at).strftime("%Y:%m:%d %H:%M:%S")
            formatted_processed_at = localtime(uploaded_image.processed_at).strftime("%Y:%m:%d %H:%M:%S")

            # Store image details in session storage
            request.session["image_id"] = uploaded_image.id
            request.session["image_name"] = uploaded_image.image_name
            request.session["uploaded_at"] = formatted_uploaded_at
            request.session["processed_at"] = formatted_processed_at
            request.session["processed_image_name"] = uploaded_image.processed_image_name

            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"output_url": f"/media/{output_filename}"}, status=200)
            
            return redirect("success")

        return render(request, "enhancer/upload.html")

    except Exception as e:
        return render(request, "enhancer/error.html", {"error_message": f"Error: {str(e)}"})

def success_page(request):
    # Retrieve session data
    image_id = request.session.get("image_id")
    image_name = request.session.get("image_name")
    uploaded_at = request.session.get("uploaded_at")
    processed_at = request.session.get("processed_at")
    processed_image_name = request.session.get("processed_image_name")

    processed_image_url = f"/media/{processed_image_name}" if processed_image_name else ""

    # Pass the details to the success page
    return render(request, "enhancer/success.html", {
        "image_id": image_id,
        "image_name": image_name,
        "uploaded_at": uploaded_at,
        "processed_at": processed_at,
        "processed_image_url": processed_image_url,
    })
