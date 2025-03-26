import os
import tempfile
import torch
import lpips
import numpy as np
from PIL import Image
from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim
from .edsr_model import apply_super_resolution  

# Initialize LPIPS model
lpips_model = lpips.LPIPS(net='alex')  # Perceptual similarity metric


def generate_test_image(size=(32, 32)):
    """Generate a small test image with patterns for variance."""
    img_array = np.zeros(size, dtype=np.uint8)
    for i in range(size[0]):
        for j in range(size[1]):
            img_array[i, j] = (i * j) % 255  # Gradient-like pattern
    return Image.fromarray(img_array, mode="L")  # Convert to grayscale


class SuperResolutionUnitTests(TestCase):
    """Unit tests for apply_super_resolution"""

    def setUp(self):
        """Create a temporary low-resolution image for testing."""
        self.test_image = generate_test_image()
        self.test_input_path = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
        self.test_output_path = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
        self.test_image.save(self.test_input_path)

    def tearDown(self):
        """Cleanup temporary files."""
        if os.path.exists(self.test_input_path):
            os.remove(self.test_input_path)
        if os.path.exists(self.test_output_path):
            os.remove(self.test_output_path)

    def test_apply_super_resolution(self):
        """Test apply_super_resolution with PSNR, SSIM, and LPIPS metrics."""
        scale = 2  # Test with 2x upscaling
        print("\n🟢 Running apply_super_resolution...")

        # Apply super-resolution
        try:
            output_path = apply_super_resolution(self.test_input_path, self.test_output_path, scale)
            print(f"✅ Super-resolution applied. Output saved at: {output_path}")

            # Validate output file exists
            self.assertTrue(os.path.exists(output_path), "❌ Output image was not created.")

            # Load images
            original = Image.open(self.test_input_path).convert("L")  # Convert to grayscale
            enhanced = Image.open(output_path).convert("L")

            # Resize original to match super-resolved image
            original_resized = original.resize(enhanced.size, Image.BICUBIC)

            # Convert to numpy arrays
            original_array = np.array(original_resized, dtype=np.float32)
            enhanced_array = np.array(enhanced, dtype=np.float32)

            # Ensure valid images
            if original_array.max() == original_array.min():
                self.skipTest("❌ Original image has no variance, SSIM undefined.")
            if enhanced_array.max() == enhanced_array.min():
                self.skipTest("❌ Enhanced image has no variance, SSIM undefined.")

            # Compute image quality metrics
            psnr_value = psnr(original_array, enhanced_array, data_range=enhanced_array.max() - enhanced_array.min())
            ssim_value = ssim(original_array, enhanced_array, data_range=enhanced_array.max() - enhanced_array.min())

            # Compute LPIPS
            original_tensor = torch.tensor(original_array).unsqueeze(0).unsqueeze(0) / 255.0
            enhanced_tensor = torch.tensor(enhanced_array).unsqueeze(0).unsqueeze(0) / 255.0
            lpips_value = lpips_model(original_tensor, enhanced_tensor).item()

            # Print output values
            print(f"🔹 PSNR: {psnr_value:.2f} dB")
            print(f"🔹 SSIM: {ssim_value:.4f}")
            print(f"🔹 LPIPS: {lpips_value:.4f} ")

            # Validate thresholds
            self.assertGreater(psnr_value, 20, "❌ PSNR is too low!")
            self.assertGreater(ssim_value, 0.5, "❌ SSIM is too low!")
            self.assertLess(lpips_value, 0.2, "❌ LPIPS is too high!")

        except Exception as e:
            self.fail(f"❌ apply_super_resolution failed: {e}")


class SuperResolutionIntegrationTests(TestCase):
    """Integration test for full pipeline (upload → process → download)"""

    def setUp(self):
        """Prepare test client and temporary test image."""
        self.client = Client()
        self.test_image = generate_test_image()
        self.test_image_path = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
        self.test_image.save(self.test_image_path)

    def tearDown(self):
        """Cleanup test image."""
        if os.path.exists(self.test_image_path):
            os.remove(self.test_image_path)

    def test_image_upload_and_super_resolution(self):
        """Test full API pipeline: Upload → Process → Download"""
        print("\n🟢 Running integration test...")

        # Upload test image
        with open(self.test_image_path, "rb") as image_file:
            uploaded_image = SimpleUploadedFile("test.png", image_file.read(), content_type="image/png")

        response = self.client.post("/home/upload/", {"image": uploaded_image, "scale": 2}, HTTP_X_REQUESTED_WITH="XMLHttpRequest", follow=True)
        self.assertEqual(response.status_code, 200, "❌ API did not return a successful response.")

        # Extract output URL
        response_data = response.json()
        self.assertIn("output_url", response_data, "❌ Output URL missing in response.")
        output_url = response_data["output_url"]
        output_path = output_url.replace("/media/", "media/")

        print(f"✅ Image processed successfully. Output URL: {output_url}")

        # Validate output file exists
        self.assertTrue(os.path.exists(output_path), "❌ Processed image file does not exist.")

        # Validate output dimensions
        output_image = Image.open(output_path)
        expected_size = (64, 64)  # Since we used scale=2
        self.assertEqual(output_image.size, expected_size, "❌ Upscaled image size is incorrect.")

        print(f"✅ Output image found at {output_path}")
        print(f"🔹 Expected size: {expected_size}, Actual size: {output_image.size}")
        print("🎯 Integration Test Passed: Full Pipeline Works!")
