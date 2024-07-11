import requests
from bs4 import BeautifulSoup

from .Premise import Premise


import os
from dotenv import load_dotenv

import time 
from urllib.parse import urlparse

load_dotenv()

class FactCheckResult:
    def __init__(self, hypothesis):
        self.premises = []
        self.hypothesis = hypothesis
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'})
        self.last_url = None
    
    def _add_premise(self, premise, hypothesis, url):
        self.premises.append(Premise(premise, hypothesis, url))

    def get_All_Premises(self):
        query = self.hypothesis
        results = self._google_custom_search(query)
        if "items" in results:
            init_premises = 0
            MAX_PREMISES = 5
            for item in results["items"]:
                if init_premises >= MAX_PREMISES:
                    break
                url = item["link"]
                snippet = item["snippet"]
                page_content = self._get_page_content(url)

                # Get the middle words from the snippet
                words = snippet.split()
                middle_index = len(words) // 2
                middle_words = words[max(0, middle_index - 2):middle_index + 3]

                if page_content is None:
                    continue
                else:
                    sentences = self._find_text_with_context(page_content, middle_words)
                    if sentences is not None and sentences.strip():
                        self._add_premise(sentences, query, url)
                        init_premises += 1

    def _google_custom_search(self, query):
        api_key = os.getenv("GOOGLE_SEARCH_API_KEY")  # Replace with your own API key
        cx = os.getenv("GOOGLE_SEARCH_ID")  # Replace with your own Custom Search Engine ID
        # Assuming google_custom_search function sends a GET request to the Google Custom Search JSON API
        maxResult = 10
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'q': query,
            'key': api_key,
            'cx': cx,
            'num': maxResult
        }
        response = requests.get(url, params=params)
        return response.json()
    
    def _google_fact_check(query, num):
        api_key = os.getenv("GOOGLE_FACT_CHECK_API")  # Replace with your own API key
        url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={query}&key={api_key}"
        
        response = requests.get(url)
        data = response.json()

        if 'claims' in data:
            return data['claims'][:num]
        else:
            return []

    def _get_page_content(self, url):
        try:
            # Inside your method
            parsed_current_url = urlparse(url)
            current_base_url = f"{parsed_current_url.scheme}://{parsed_current_url.netloc}"

            parsed_last_url = urlparse(self.last_url)
            last_base_url = f"{parsed_last_url.scheme}://{parsed_last_url.netloc}"

            if current_base_url == last_base_url:  # Compare base URLs instead of full URLs
                time.sleep(0.5)

            response = self.session.get(url, timeout=2)
            self.last_url = url  # Update last_url with the full URL for future comparisons
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                text = soup.get_text()
                return text.replace('\n', ' ')
            else:
                print(f"Request failed with status code: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")
            return None

    def _find_text_with_context(self, text, words):
        words_to_find = " ".join(words)
        start_index = text.find(words_to_find)
        
        if start_index == -1:
            return None

        start_of_context = text.rfind('.', 0, start_index) + 1
        end_of_context = text.find('.', start_index + len(words_to_find))

        if start_of_context == -1:
            start_of_context = 0
        if end_of_context == -1:
            end_of_context = len(text)

        return text[start_of_context:end_of_context].strip()

    def to_json(self):
        return {
            'hypothesis': self.hypothesis,
            'premises': [premise.to_json() for premise in self.premises]
        }

