# For scraping
import requests
from bs4 import BeautifulSoup

# For NLI
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

# For query building 
# from openai import OpenAI
# client = OpenAI()
import re

# env
import os
from dotenv import load_dotenv

load_dotenv()

class Premise:
    def __init__(self, premise, hypothesis):
        self.premise = premise
        self.relationship = self.relationship = self._determine_relationship_premise_hypothesis(premise, hypothesis)
    
    # NLI task - to be change to xlm-roberta-nli for entailemnt, contradiction, neutral
    def _determine_relationship_premise_hypothesis(self, premise, hypothesis):
        model = AutoModelForSequenceClassification.from_pretrained("ctu-aic/xlm-roberta-large-squad2-ctkfacts_nli")
        tokenizer = AutoTokenizer.from_pretrained("ctu-aic/xlm-roberta-large-squad2-ctkfacts_nli")

        inputs = tokenizer.encode_plus(premise, hypothesis, return_tensors='pt')

        # Step 2: Pass the inputs through the model without computing gradients
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
        
        predicted_class = torch.argmax(logits, dim=1).item()
        labels = ["entailment", "neutral", "contradiction"]
        result = labels[predicted_class]

        return result

    def to_json(self):
        return {
            'premise': self.premise,
            'relationship': self.relationship
        }


class FactCheckResult:
    def __init__(self, hypothesis):
        self.premises = []
        self.hypothesis = hypothesis
    
    def _add_premise(self, premise, hypothesis):
        self.premises.append(Premise(premise, hypothesis))

    def get_All_Premises(self):
        query = self.hypothesis
        results = self._google_custom_search(query)
        if "items" in results:
            for item in results["items"]:
                url = item["link"]
                snippet = item["snippet"]
                page_content = self._get_page_content(url)

                # Get the middle words from the snippet
                words = snippet.split()
                middle_index = len(words) // 2
                middle_words = words[max(0, middle_index - 2):middle_index + 3]
                
                # Get snippet result of google
                page_content = self._get_page_content(url)
                sentences = self._find_text_with_context(page_content, middle_words)

                self._add_premise(sentences, query)

    def _google_custom_search(self, query):
        api_key = os.getenv("GOOGLE_SEARCH_API_KEY")  # Replace with your own API key
        cx = os.getenv("GOOGLE_SEARCH_ID")  # Replace with your own Custom Search Engine ID
        # Assuming google_custom_search function sends a GET request to the Google Custom Search JSON API
        maxResult = 5
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'q': query,
            'key': api_key,
            'cx': cx,
            'num': maxResult
        }
        response = requests.get(url, params=params)
        return response.json()
    
    def _get_page_content(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()
        return text.replace('\n', ' ')

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


# query processing
class query_processing:
    def __init__(self, query):
        self.query = query
        self.dividedQueries = self._query_builder(query)
    
    # still no api key
    def _query_builder(self, text):

        
        prompt = f"I need to generate search queries based on the following text. Please create multiple search queries that I can use in Google to find relevant information. \n Text: \n \"\"\" {text} \"\"\" \n Search Queries:\n1.\n2.\n3.\n4.\n5."
        

        output = self._query(prompt)

        # Extract the generated text from the response
        generated_text = output.choices[0].text.strip()

        # Split the generated text by numbers
        parts = re.split(r'\d+', generated_text)

        # Return the parts as the queries for fact-checking
        return parts
    

    # llama api url
    @staticmethod
    def _query(prompt):
        API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
        token = os.getenv("HUGGING_FACE_TOKEN")
        headers = {"Authorization": f"Bearer {token}"}

        payload = {
            "inputs": prompt,
        }

        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()


    def get_divided_queries(self):
        return self.dividedQueries



def main():
    query = input("Enter your search query: ")

    # For query building
    queryBuilder = query_processing(query)
    claims = queryBuilder.get_divided_queries()

    maxClaimsToCheck = 3
    FactCheckResult = []
    for i in range(min(maxClaimsToCheck, len(claims))):

        claim = claims[i]
        factClass = FactCheckResult(claim)
        factClass.get_All_Premises()

        FactCheckResult.append(factClass.to_json())

    # return the list of FactCheckResult objects
    return FactCheckResult
     




# fact check explorer of google ---- i want to use semantic search
def google_fact_check(query, num):
    api_key = os.getenv("GOOGLE_FACT_CHECK_API")  # Replace with your own API key
    url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?query={query}&key={api_key}"
    
    response = requests.get(url)
    data = response.json()

    if 'claims' in data:
        return data['claims'][:num]
    else:
        return []


if __name__ == "__main__":
    main()  
    