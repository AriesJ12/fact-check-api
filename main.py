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

@app.get("/api/v1/factCheck")
def fact_check(content: str):
    try:
        result = main(content)
        return {"content": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
