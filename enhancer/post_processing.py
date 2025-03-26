import cv2
import numpy as np

def apply_post_processing(image):
    '''
    Adaptive post-processing based on image characteristics.
    Ensures no over-processing by selectively applying enhancements.
    '''
    # Convert to grayscale to analyze features
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Compute contrast using standard deviation
    contrast = np.std(gray)
    
    # Compute sharpness using Laplacian variance
    sharpness = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    # Adaptive sharpening (only if the image is not already sharp)
    if sharpness < 100:  # Threshold to detect blurry images
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        image = cv2.filter2D(image, -1, kernel)

    # Adaptive contrast enhancement (only if contrast is low)
    if contrast < 50:  # Threshold to detect low contrast
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        image = cv2.merge((l, a, b))
        image = cv2.cvtColor(image, cv2.COLOR_LAB2BGR)

    # Convert back to uint8 for proper saving
    image = np.clip(image, 0, 255).astype(np.uint8)

    return image