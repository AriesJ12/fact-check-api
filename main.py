from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fact_check import main

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {1: "Server is up and running"}

@app.post("/api/v1/factCheck")
def fact_check(content: str):
    try:
        result = main_fact_check(content)
        return {"content": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/factCheckWithoutQueries")
def fact_check_without_query(content:str):
    try:
        result = main_fact_check_without_query(content)
        return {"content": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/claimDetection")
def claim_detection(content:str)
    try:
        result = main_claim_detection(content)
        return {"content": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
