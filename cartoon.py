import cv2
import numpy as np

def cartoonize(img_path):
    img = cv2.imread(img_path)
    img = cv2.resize(img, (800, 800))
    
    # ---- Remove Background ----
    mask = np.zeros(img.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    rect = (50, 50, 750, 750)
    
    cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    
    # ---- Convert to Grayscale ----
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # ---- Pencil Sketch Effect ----
    # Invert image
    inverted = cv2.bitwise_not(gray)
    
    # Blur the inverted image
    blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
    
    # Invert the blurred image
    inverted_blur = cv2.bitwise_not(blurred)
    
    # Create sketch
    sketch = cv2.divide(gray, inverted_blur, scale=270.0)
    
    # Enhance contrast
    sketch = cv2.normalize(sketch, None, 50, 255, cv2.NORM_MINMAX)
    
    # Apply sharpening
    kernel = np.array([[-1, -1, -1],
                       [-1,  9, -1],
                       [-1, -1, -1]])
    sketch = cv2.filter2D(sketch, -1, kernel)
    
    # ---- Apply White Background ----
    # Create white canvas
    white_canvas = np.ones_like(sketch) * 255
    
    # Only show sketch where person is (using mask)
    final_sketch = np.where(mask2 == 1, sketch, 255).astype('uint8')
    
    return final_sketch