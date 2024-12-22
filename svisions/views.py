from django.shortcuts import render
from .forms import ImageUploadForm

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'svisions/upload_success.html')
    else:
        form = ImageUploadForm()
    return render(request, 'svisions/upload_image.html', {'form': form})
