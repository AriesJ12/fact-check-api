from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fact_check import main_fact_check, main_fact_check_without_query, main_claim_detection
from classes.Summarize import SummarizerService
import nltk


import io
import requests
import uvicorn
import pytesseract
from PIL import Image

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["Content-type"],
)

# parang delikado to, for some reaeson
from classes.Config import Config
app.config = Config()

@app.on_event("startup")
async def download_nltk_resources():
    nltk.download("punkt")

@app.get("/")
async def root():
    return {1: "Server is up and running"}

@app.get("/api/v1/summarizer")
async def summarize(request: SummarizerService.SummarizeRequest):
    return await SummarizerService.summarize(request)


@app.get("/api/v1/factCheck")
async def fact_check(content: str):
    try:
        result = main_fact_check(content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/factCheckWithoutQueries")
async def fact_check_without_query(content:str):
    try:
        result = main_fact_check_without_query(content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/claimDetection")
async def claim_detection(content:str):
    try:
        result = main_claim_detection(content)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
'''
OCR
'''

@app.post("/extract_text_from_url")
async def extract_text_from_url(url: str):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=422, detail="Invalid image URL")
        image = Image.open(io.BytesIO(response.content))
        text = pytesseract.image_to_string(image)
        return {"text": text.replace("\n", " ").strip()}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

@app.get("/ocr")
async def ocr(image_url: str):

    try:
        response = requests.get(image_url)
        if response.status_code != 200:
            raise HTTPException(status_code=422, detail="Invalid image URL")
        image = Image.open(io.BytesIO(response.content))
        text = pytesseract.image_to_string(image)
        
        return {"text": text.replace("\n", " ").strip()}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
