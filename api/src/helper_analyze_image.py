import cv2
import numpy as np
from pytesseract import pytesseract


def preprocess_image(image):
    image = cv2.resize(image, (600, 400))
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    return binary


def extract_text(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    text = pytesseract.image_to_string(gray).strip()
    return text if text else None


def calculate_letter_spacing(contours):
    spacings = []
    for i in range(1, len(contours)):
        x_prev, _, w_prev, _ = cv2.boundingRect(contours[i - 1])
        x, _, _, _ = cv2.boundingRect(contours[i])
        spacing = x - (x_prev + w_prev)
        spacings.append(spacing)
    if spacings:
        avg_spacing = np.mean(spacings)
        if avg_spacing < 5:
            return "tight"
        elif avg_spacing < 10:
            return "normal"
        else:
            return "wide"
    return "unknown"
