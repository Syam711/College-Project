from super_image import EdsrModel, ImageLoader
from PIL import Image
import torch

def apply_super_resolution(image_path, output_path, scale):
    try:
        # Check if GPU is available, otherwise use CPU
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Load the model and move it to the selected device
        model = EdsrModel.from_pretrained('edsr-base', scale=scale).to(device)
        
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
