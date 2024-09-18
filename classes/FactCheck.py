import requests
# from bs4 import BeautifulSoup

from .Premise import Premise


import os
from dotenv import load_dotenv


from classes.Counter import Counter
load_dotenv()

class FactCheckResult:
    def __init__(self, query, hypothesis):
        self.query = query
        self.hypothesis = hypothesis
        self.premiseClass = Premise(hypothesis=hypothesis)
    
    def __add_premise(self, premise, url, title, date):
        self.premiseClass.add_premise(premise=premise, url=url, title=title, date=date)

    def get_All_Premises(self):
        query = self.query
        results = self.__google_custom_search(query)
        if "items" in results:
            init_premises = 0
            MAX_PREMISES = 10
            for item in results["items"]:
                if init_premises >= MAX_PREMISES:
                    break
                url = item["link"]
                title = item.get("title", "No title available")
        
                date = "No date available"
                if "pagemap" in item:
                    pagemap = item["pagemap"]
                    if "metatags" in pagemap and len(pagemap["metatags"]) > 0:
                        date = pagemap["metatags"][0].get("article:published_time", date)
                    elif "newsarticle" in pagemap and len(pagemap["newsarticle"]) > 0:
                        date = pagemap["newsarticle"][0].get("datepublished", date)

                snippet = item["snippet"]
                sentences = snippet
                
                if sentences is not None and sentences.strip():
                    self.__add_premise(premise=sentences, url=url, title=title, date=date)
                    init_premises += 1
            
            return self.premiseClass.determine_all_relationship_premise_hypothesis()

    def __google_custom_search(self, query):
        counter_instance = Counter(db_file="google_calls.db", max_calls_per_day=80)
        counter_instance.update_counter()
        api_key = os.getenv("GOOGLE_SEARCH_API_KEY")  # Replace with your own API key
        cx = os.getenv("GOOGLE_SEARCH_ID")  # Replace with your own Custom Search Engine ID
        # Assuming google_custom_search function sends a GET request to the Google Custom Search JSON API
        maxResult = 10 # this is having an error, if its more than 10; it will break
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'q': query,
            'key': api_key,
            'cx': cx,
            'num': maxResult
        }
        try:
            response = requests.get(url, params=params)
            
            # This will raise an HTTPError if the status code is 4xx or 5xx
            response.raise_for_status()

            # If the response is successful, return the JSON data
            return response.json()

        except requests.exceptions.HTTPError as http_err:
            # Regardless of the specific error, raise an exception with the message "Daily limit reached"
            raise Exception("Daily limit reached") from http_err


    def to_json(self):
        return {
            'hypothesis': self.hypothesis,
            'premises': self.premiseClass.get_all_premises_with_relationship()
        }
    
    def get_processed_premises(self):
        return self.premiseClass.get_all_premises_with_relationship() #change here
