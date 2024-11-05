import json
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from PIL import Image
import pytesseract
import os
from dotenv import load_dotenv
from io import BytesIO
import cv2
import numpy as np

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = ChatOpenAI(model_name="gpt-4o", openai_api_key=openai_api_key)

prompt_template = """
Based on the following text characteristics, suggest the top 3 font types that most closely match the description.

Focus on:
- Character thickness (thin, regular, bold)
- Letter shape (rounded, geometric, angular)
- X-height (proportionally high, medium, or low)
- Spacing between letters (tight, normal, wide)
- Serif presence (serif, sans-serif)

Please provide the font names in a ranked order with a confidence level for each font. If no text is detected, respond with {{ "fonts": ["unknown"], "confidence": "none" }}.

Text Characteristics:
{image_data}
Extracted Text (if any):
{text}
"""
prompt = PromptTemplate(input_variables=["image_data", "text"], template=prompt_template)

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

@app.post("/api/analyze-image")
async def analyze_image_endpoint(file: UploadFile = File(...)):
    try:
        image = Image.open(BytesIO(await file.read()))
        image_np = np.array(image)

        character_thickness, letter_shape, spacing_between_letters, serif_presence, x_height = extract_font_features(image_np)
        text = extract_text(image_np)

        if text is None:
            text = "No text detected"

        image_data = f"""
        Character thickness: {character_thickness}
        Letter shape: {letter_shape}
        X-height: {x_height}
        Spacing between letters: {spacing_between_letters}
        Serif presence: {serif_presence}
        """
        filled_prompt = prompt.format(image_data=image_data, text=text)

        result = llm.invoke(filled_prompt)

        response_content = json.loads(result.content) if hasattr(result, 'content') else str(result)

        return JSONResponse(content={"result": response_content})

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Image file not found.")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Value error: {ve}")
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
