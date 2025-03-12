from PIL import Image

def resize_image(image_path, output_path, width, height):
    try:
        image = Image.open(image_path)
        resized_image = image.resize((width, height), Image.LANCZOS)
        resized_image.save(output_path)
        return output_path
    except Exception as e:
        raise RuntimeError(f"Error resizing image: {str(e)}")
