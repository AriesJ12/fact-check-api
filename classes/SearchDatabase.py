import requests
from elasticsearch import Elasticsearch, helpers
import numpy as np
import re
import os
from dotenv import load_dotenv


from classes.Counter import Counter
load_dotenv()

class SearchDatabase:

    def __init__(self, query, mode):
        self.query = query
        self.mode = mode
        pass
    
    def get_results(self):
        if self.mode == "google":
            return self.__google_custom_search(self.query)
        elif self.mode == "onlineDatabase":
            return self.__elastic_search(self.query)
        else:
            return {"result" : "Invalid mode"}
    
    # online database/elastic search
    def __elastic_search(self, query):
        index_name = "medical_articles"
        username = "elastic"
        api_key = os.getenv("ELASTIC_PASSWORD")
        url = os.getenv("ELASTIC_URL")
        es = Elasticsearch(
            url,
            basic_auth=(username, api_key),
            verify_certs=False
        )
        # change this
        txt_file_path = "./asset/new_extracted_terms.txt"
        
        # Step 1: Read the content of the text file
        try:
            with open(txt_file_path, 'r') as file:
                content = file.read()
        except FileNotFoundError:
            print(f"File not found: {txt_file_path}")
            return []
        except Exception as e:
            print(f"Error reading file: {e}")
            return []
        
        # Step 2: Clean the content by removing quotes and commas
        words = re.findall(r'\b\w+\b', content)
        
        # Convert words to lowercase
        words = [word.lower() for word in words]
        
        # Convert query to lowercase
        query_lower = query.lower()
        
        # Step 3: Initialize results
        results = []

        # Step 4: Check if any of the words from the text file are in the query
        for word in words:
            # Use word boundaries to match whole words only
            if re.search(r'\b' + re.escape(word) + r'\b', query_lower):
                # Step 5: Proceed with the Elasticsearch query
                body = {
                    "query": {
                        "query_string": {
                            "query": query,
                            "fields": ["title","altTitles", "fullSummary", "meshTerms", "groupNames"]
                        }
                    },
                    "highlight": {
                        "fields": {
                            "fullSummary": {},
                        }
                    }
                }

                try:
                    response = es.search(index=index_name, body=body)
                except Exception as e:
                    print(f"Server Down on Online Database")
                    return []

                # Extract hits and their highlighted snippets
                for hit in response['hits']['hits']:
                    # Get the original document
                    doc = hit['_source']
                    
                    # Add highlighted snippets if available
                    if 'highlight' in hit:
                        highlighted_snippets = hit['highlight']
                        # Remove HTML tags from snippets
                        snippets = {field: [re.sub(r'<.*?>', '', snippet) for snippet in highlighted_snippets[field]] for field in highlighted_snippets}
                        results.append({
                            'document': doc,
                            'snippets': snippets
                        })
                    else:
                        results.append({'document': doc, 'snippets': None})

                # Return results if at least one word matched
                return self.__format_elastic_results(results=results)

        # If no words matched, return an empty list
        return results

    def __format_elastic_results(self, results):
        formatted_results = []
        for result in results:
            doc = result["document"]
            snippets = self.__generate_better_snippets(result["snippets"])
            formatted_results.append({
                "premise": snippets,
                "url": doc.get("url", "No URL available"),
                "title": doc.get("title", "No title available"),
                "date": doc.get("date", "No date available")
            })
        return formatted_results
    
    def __generate_better_snippets(self, snippets):
        # Handle both string and dict for snippets
        if isinstance(snippets, dict):
            # Assuming the relevant text is in 'fullSummary' key
            full_summary = snippets.get('fullSummary', [])
            if isinstance(full_summary, list):
                snippets = ' '.join(full_summary)  # Join list into a single string
            else:
                snippets = str(full_summary)  # Convert to string if not a list
        elif not isinstance(snippets, str):
            raise TypeError("Snippets should be a string or a dictionary containing a string.")
        
        return snippets

    # google
    def __format_google_results(self, results):
        formatted_results = []
        if "items" in results:
            for item in results["items"]:
                url = item["link"]
                title = item.get("title", "No title available")
                date = "No date available"
                if "pagemap" in item:
                    pagemap = item["pagemap"]
                    if "metatags" in pagemap and len(pagemap["metatags"]) > 0:
                        date = pagemap["metatags"][0].get("citation_publication_date", date)
                    elif "newsarticle" in pagemap and len(pagemap["newsarticle"]) > 0:
                        date = pagemap["newsarticle"][0].get("datepublished", date)
                snippet = item["snippet"]
                formatted_results.append({
                    "premise": snippet,
                    "url": url,
                    "title": title,
                    "date": date
                })
        return formatted_results

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
            return self.__format_google_results(response.json())

        except requests.exceptions.HTTPError as http_err:
            # Regardless of the specific error, raise an exception with the message "Daily limit reached"
            raise Exception("Daily limit reached") from http_err