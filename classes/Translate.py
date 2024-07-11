import os
import requests
from dotenv import load_dotenv

load_dotenv()


class Translate:
    def __init__(self):
        pass


    def tagalog_to_english(self, text):
        """
        Translates the given text to the target language.
        
        Args:
            text (str): The input text to translate.
        
        Returns:
            str: The translated text.
        """

        api_key = os.getenv("HUGGING_FACE_TOKEN")

        API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-tl-en"
        headers = {"Authorization": "Bearer " + api_key}

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()
            
        output = query({
            "inputs": text,
        })
        return output["translation_text"]

        

