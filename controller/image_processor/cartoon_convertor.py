import cv2
import numpy as np


def cartoon_effect(img_path, output_path=None):
    """
    Convert a photo to cartoon style image with better color preservation
    and more natural edge detection
    
    Parameters:
    img_path (str): Path to the input image
    output_path (str, optional): Path to save the output image. If None, displays the image instead.
    
    Returns:
    numpy.ndarray: The cartoon-style image
    """
    # Read the image
    img = cv2.imread(img_path)
    if img is None:
        raise ValueError(f"Could not read image at {img_path}")
    
    # Create a working copy
    result = img.copy()
    
    # Step 1: Convert to grayscale and apply bilateral filter
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.medianBlur(gray, 5)
    
    # Step 2: Edge detection with more control
    # Using Canny edge detector instead of adaptive threshold for better control
    edges = cv2.Canny(gray_blur, 50, 150)
    edges = cv2.dilate(edges, None)
    edges = cv2.bitwise_not(edges)  # Invert so edges are black, background is white
    
    # Step 3: Smooth colors using bilateral filter
    # Reduce noise while keeping edges sharp
    color = cv2.bilateralFilter(img, 9, 300, 300)
    
    # Step 4: Create cartoon by blending color image with edges
    # Convert edges to 3-channel for blending
    edges_3channel = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    
    # Blend the color image with edges
    # Using the edges as a mask to preserve more color information
    cartoon = cv2.bitwise_and(color, edges_3channel)
    
    # Step 5: Optional color quantization for more cartoon-like effect
    # Use fewer clusters for more dramatic cartoon effect
    data = np.float32(cartoon).reshape((-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
    k = 8  # Number of colors - adjust to taste
    _, labels, centers = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    result = centers[labels.flatten()].reshape(cartoon.shape)
    
    result = cv2.convertScaleAbs(result, alpha=1.1, beta=10)
    

    if output_path:
        cv2.imwrite(output_path, result)
        print(f"Cartoon image saved to {output_path}")
    
    return result

