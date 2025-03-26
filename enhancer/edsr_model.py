from super_image import EdsrModel, ImageLoader
from PIL import Image
import torch
import cv2
import numpy as np
from .post_processing import apply_post_processing

def apply_super_resolution(image_path, output_path, scale):
    try:
        # Check if GPU is available, otherwise use CPU
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Load the model and move it to the selected device
        model_name = f"eugenesiow/edsr-base"  # Pretrained EDSR model
        model = EdsrModel.from_pretrained(model_name, scale=scale).to(device)
        
        # Load input image
        image = Image.open(image_path)
        inputs = ImageLoader.load_image(image).to(device)  # Move inputs to GPU if available

        # Perform inference
        model.eval()
        with torch.no_grad():
            preds = model(inputs)

        # Save output image
        ImageLoader.save_image(preds, output_path)
        
        return output_path

    except Exception as e:
        raise RuntimeError(f"Error applying super-resolution: {str(e)}")

def super_resolve(image_path, scale=2):
    # Load image
    image = cv2.imread(image_path)
    
    # Placeholder for super-resolution (replace with actual EDSR inference)
    height, width = image.shape[:2]
    new_size = (width * scale, height * scale)
    sr_image = cv2.resize(image, new_size, interpolation=cv2.INTER_CUBIC)

    # Apply post-processing for quality enhancement
    enhanced_image = apply_post_processing(sr_image)

    return enhanced_image