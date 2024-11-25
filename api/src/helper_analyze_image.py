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


def extract_font_features(image):
    binary = preprocess_image(image)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    thicknesses = []
    heights = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        thicknesses.append(h)
        heights.append(h)

    if thicknesses:
        avg_thickness = np.mean(thicknesses)
        if avg_thickness < 10:
            character_thickness = "thin"
        elif avg_thickness < 20:
            character_thickness = "regular"
        else:
            character_thickness = "bold"
    else:
        character_thickness = "unknown"

    if heights:
        avg_height = np.mean(heights)
        if avg_height < 15:
            x_height = "low"
        elif avg_height < 25:
            x_height = "medium"
        else:
            x_height = "high"
    else:
        x_height = "unknown"

    spacing_between_letters = calculate_letter_spacing(contours)
    serif_presence = "sans-serif"
    letter_shape = "rounded"

    return character_thickness, letter_shape, spacing_between_letters, serif_presence, x_height
