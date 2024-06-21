from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fact_check import main

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["Content-Type"],
)

@app.get("/")
def root():
    return {1: "Server is up and running"}

@app.get("/api/v1/factCheck")
def detect(content: str):
    return {'result': main(content)}