from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from PIL import Image
import pytesseract
import os
from dotenv import load_dotenv
from io import BytesIO

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

llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key)

prompt_template = """
Analyze the following text image and try to identify the most likely font type. Focus specifically on details such as:

- Character thickness (thin, regular, bold)
- Letter shape (rounded vs. angular)
- Spacing between letters
- Serif presence (serif vs. sans-serif)

Provide the font name in JSON format with a confidence score, if possible. Answer format: {{ "font": "font_name", "confidence": "high/medium/low" }}.

Text Content:
{text_content}
"""
prompt = PromptTemplate(input_variables=["text_content"], template=prompt_template)

chain = prompt | llm

@app.post("/api/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    try:
        image = Image.open(BytesIO(await file.read()))
        extracted_text = pytesseract.image_to_string(image)

        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="No text found in the image.")

        result = chain.invoke({"text_content": extracted_text})

        response_content = result.content if hasattr(result, 'content') else str(result)
        return JSONResponse(content={"result": response_content})

    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
