import numpy as np # type: ignore
import matplotlib.pyplot as plt # type: ignore
import cv2 # type: ignore #image processing technique 
from scipy import ndimage # type: ignore #additional image processing technique

class ImageEnhancer:
    def __init__(self, image_path=None):
        self.image = cv2.imread(image_path) if image_path else self.create_sample_image()
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
     
    def create_sample_image(self):
        """Create a sample image for demonstration"""
        img = np.zeros((200, 200, 3), dtype=np.uint8)
        cv2.rectangle(img, (50, 50), (150, 150), (255, 255, 255), -1)
        cv2.circle(img, (100, 100), 40, (128, 128, 128), -1)
        return img

    def show(self, images, titles, figsize=(15, 5)):
        """Display multiple images"""
        fig, axes = plt.subplots(1, len(images), figsize=figsize)
        for ax, img, title in zip(axes, images, titles):
            ax.imshow(img)
            ax.set_title(title)
            ax.axis('off')
        plt.tight_layout()
        plt.show()

    # Point Processing Methods
    def brightness(self, value):
        return np.clip(self.image.astype(float) + value, 0, 255).astype(np.uint8)
    
    def contrast(self, factor):
        return np.clip(factor * (self.image.astype(float) - 128) + 128, 0, 255).astype(np.uint8)
    
    def gamma(self, gamma):
        return (255 * (self.image.astype(float) / 255) ** (1/gamma)).astype(np.uint8)
    
    def negative(self):
        return 255 - self.image

    # Spatial Filtering Methods
    def mean_filter(self, size=3):
        kernel = np.ones((size, size)) / (size * size)
        return cv2.filter2D(self.image, -1, kernel)
    
    def gaussian_filter(self, size=3, sigma=1):
        return cv2.GaussianBlur(self.image, (size, size), sigma)
    
    def median_filter(self, size=3):
        return cv2.medianBlur(self.image, size)
    
    def sobel_edges(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        magnitude = np.sqrt(sobelx**2 + sobely**2)
        return (255 * magnitude / np.max(magnitude)).astype(np.uint8)
    
    def sharpen(self):
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        return cv2.filter2D(self.image, -1, kernel)

def demo():
    """Demonstrate all techniques"""
    enhancer = ImageEnhancer()
    
    # Point Processing Examples
    bright = enhancer.brightness(50)
    dark = enhancer.brightness(-30)
    high_contrast = enhancer.contrast(1.8)
    low_contrast = enhancer.contrast(0.6)
    gamma_low = enhancer.gamma(0.5)
    gamma_high = enhancer.gamma(2.0)
    negative = enhancer.negative()
    
    print("Point Processing Results:")
    enhancer.show([enhancer.image, bright, dark, high_contrast, low_contrast, 
                   gamma_low, gamma_high, negative],
                  ['Original', 'Bright', 'Dark', 'High Contrast', 'Low Contrast',
                   'Gamma 0.5', 'Gamma 2.0', 'Negative'],   
                  figsize=(18, 4))
    
    # Spatial Filtering Examples
    mean = enhancer.mean_filter(5)
    gaussian = enhancer.gaussian_filter(5, 1)
    median = enhancer.median_filter(3)
    edges = enhancer.sobel_edges()
    sharp = enhancer.sharpen()
    
    print("Spatial Filtering Results:")
    enhancer.show([enhancer.image, mean, gaussian, median, edges, sharp],
                  ['Original', 'Mean Filter', 'Gaussian', 'Median', 'Sobel Edges', 'Sharpened'],
                  figsize=(15, 4))

if __name__ == "__main__":
    demo()