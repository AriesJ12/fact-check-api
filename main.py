from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fact_check import main_fact_check, main_fact_check_without_query, main_claim_detection
from classes.NLISingleton import NLISingleton
from classes.ClaimDetection import ClaimDetection

# rosgen
# import os
# import io
# import uvicorn
# import pytesseract
# from PIL import Image
# import image_preprocessing as processing
# import numpy as np

'''
Install Tesseract OCR for Windows
'''
# home_dir = os.path.expanduser("~")
# pytesseract.pytesseract.tesseract_cmd = os.path.join(home_dir, 'AppData', 'Local', 'Programs', 'Tesseract-OCR', 'tesseract.exe')
# pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\asus\AppData\\Local\\Programs\\Tesseract-OCR\tesseract.exe'

# bruce
import nltk
import json
import random
import requests
from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel
from sumy.nlp.stemmers import Stemmer
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.parsers.html import HtmlParser


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["Content-type"],
)

@app.before_event("startup")
async def start_up():
    nltk.download("punkt")
    nlisingleton = NLISingleton()
    claimdetection = ClaimDetection()

@app.get("/")
async def root():
    return {1: "Server is up and running"}


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

# @app.post("/api/v1/extract_text_from_url")
# async def extract_text_from_url(url: str):
#     try:
#         response = requests.get(url)
#         if response.status_code != 200:
#             raise HTTPException(status_code=422, detail="Invalid image URL")
#         image = Image.open(io.BytesIO(response.content))
#         text = pytesseract.image_to_string(image)
#         return {"text": text.replace("\n", " ").strip()}
#     except Exception as e:
#         raise HTTPException(status_code=422, detail=str(e))

# @app.get("/api/v1/ocr")
# async def ocr(image_url: str):

#     try:
#         response = requests.get(image_url)
#         if response.status_code != 200:
#             raise HTTPException(status_code=422, detail="Invalid image URL")
        
#         # image = Image.open(io.BytesIO(response.content))
        
#         # Create a byte string buffer
#         byte_string = io.BytesIO(response.content)
        
#         # Validate image
#         try:
#             image = Image.open(byte_string)
#         except:
#             raise read_exception("Invalid image file")

#         # Convert image to numpy array
#         image_array = np.asarray(image)


#         # text = pytesseract.image_to_string(image)
#         text: str = processing.apply_image_processing(image_array)
        
#         return {"text": text.replace("\n", " ").strip()}
#     except Exception as e:
#         raise HTTPException(status_code=422, detail=str(e))


'''
health tips
'''

class SummarizeRequest(BaseModel):
    data: List[Optional[str]]

async def summarize(request: SummarizeRequest):
    language = "english"
    sentence_count, input_, *rest = request.data
    parser = HtmlParser.from_url(input_, Tokenizer(language))
    stemmer = Stemmer(language)
    summarizer = Summarizer(stemmer)
    summary_sentences = summarizer(parser.document, sentence_count)
    summary = " ".join([str(sentence) for sentence in summary_sentences])
    
    return summary

@app.get("/api/v1/health_tips")
async def health_tips(param: str):
    data = await get_list_and_random(param)
    id = data.get("RandomId")
    result = await get_data(id)

    summary_request = SummarizeRequest(
        data=["2", result["link"]]
    )
    summary = await summarize(summary_request)

    result["content"] = summary
    
    # Debug
    print(json.dumps(result, indent=5))
    return result

async def get_data(topic_id: int):
    url = f"https://health.gov/myhealthfinder/api/v3/topicsearch.json?TopicId={topic_id}&Lang=en"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Navigate through the keys: Result -> Resources -> Resource 
        result = data.get("Result", {})
        resources = result.get("Resources", {})
        resource = (
            resources.get("Resource", {})[0]
            if isinstance(resources.get("Resource"), list) and resources.get("Resource")
            else None
        )
        
        if resource:
            title = resource.get("Title")
            lastUpdated = resource.get("LastUpdate")
            link = resource.get("AccessibleVersion")
            lastUpdatedInt = int(lastUpdated)
            lastUpdatedDate = datetime.fromtimestamp(lastUpdatedInt, timezone.utc)
            lastUpdatedFormatted = lastUpdatedDate.strftime("%B %d, %Y")
           
        else:
            return {"error": "No resource found"}       

        data = {
            "LastUpdated": lastUpdatedFormatted,
            "title": title,
            "link": link,
        }
        # Debug
        # print(json.dumps(data, indent=5))
        return data
    else:
        print({"error": "Failed to fetch data from the health.gov API"})

async def get_list_and_random(
    topic_id: int = Query(..., description="Topic ID to filter resources"),
    id: str = Query(None, description="Filter resources by Id"),
):
    url = f"https://health.gov/myhealthfinder/api/v3/topicsearch.json?lang=en&categoryId={topic_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data: {str(e)}")

    data = response.json()
    result = data.get("Result", {})
    resources = result.get("Resources", {})
    resource_list = resources.get("Resource", [])

    ids = [resource.get("Id") for resource in resource_list if "Id" in resource]

    if not ids:
        raise HTTPException(status_code=404, detail="No IDs found in the resource list")

    random_id = random.choice(ids)

    data = {
        "Ids": ids,
        "TotalIds": len(ids),
        "RandomId": random_id,
    }
    # Debug
    # print(json.dumps(data, indent=4))
    return data

