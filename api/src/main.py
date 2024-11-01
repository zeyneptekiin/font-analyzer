from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import openai
from config import OPENAI_API_KEY

app = FastAPI()

openai.api_key = OPENAI_API_KEY

PROMPT = """
Identify all text elements in the image and determine the font type used for each.
Label each text block as text_1, text_2, etc., and assign the corresponding font name as font1, font2, in JSON format.
For example, output as { 'text_1': 'font1', 'text_2': 'font2' }.
"""

@app.post("/api/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    image_data = await file.read()

    response = openai.Image.create(
        file=image_data,
        prompt=PROMPT,
        n=1,
        size="1024x1024",
        response_format="json"
    )

    return JSONResponse(content=response)
