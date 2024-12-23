import json
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from PIL import Image
import os
from dotenv import load_dotenv
from io import BytesIO
import numpy as np
from .helper_analyze_image import (extract_text, extract_font_features)

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
