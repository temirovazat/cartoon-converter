import cv2
import numpy as np


def read_img(input_path: str) -> np.ndarray:
    """Reads an image from disk and returns it as a numpy array with RGB color channels."""
    img = cv2.cvtColor(cv2.imread(input_path), cv2.COLOR_BGR2RGB)
    return img


def edge_detection(img: np.ndarray, line_width: int, blur: int) -> np.ndarray:
    """Performs edge detection on the input image using adaptive thresholding."""
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray_blur = cv2.medianBlur(gray, blur)
    edges = cv2.adaptiveThreshold(
        gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, line_width, blur
    )
    return edges


def color_quantisation(img: np.ndarray, k: int) -> np.ndarray:
    """Quantize the colors of the input image to k distinct colors."""
    data = np.float32(img).reshape((-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
    ret, label, center = cv2.kmeans(
        data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS
    )
    center = np.uint8(center)
    result = center[label.flatten()]
    result = result.reshape(img.shape)
    return result
