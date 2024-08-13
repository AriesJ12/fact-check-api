from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fact_check import main_fact_check, main_fact_check_without_query, main_claim_detection
from classes.Summarize import SummarizerService
import nltk

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["Content-type"],
)

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
    
