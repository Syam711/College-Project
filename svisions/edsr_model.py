from super_image import EdsrModel, ImageLoader
from PIL import Image
import torch

def apply_super_resolution(image_path, output_path, scale):
    try:
        image = Image.open(image_path)

        device = torch.device('cpu')
        model = EdsrModel.from_pretrained('edsr-base', scale=scale).to(device)
        model.load_state_dict(torch.load(f'edsr-base/pytorch_model_{scale}x.pt', map_location=torch.device('cpu')))
        model.eval()
        
        inputs = ImageLoader.load_image(image)
        
        with torch.no_grad():
            preds = model(inputs)
        
        ImageLoader.save_image(preds, output_path)
        
        return output_path
    except Exception as e:
        raise RuntimeError(f"Error applying super-resolution: {str(e)}")
