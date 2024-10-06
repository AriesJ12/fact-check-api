from elasticsearch import Elasticsearch, helpers
import os
from dotenv import load_dotenv

load_dotenv()


class ElasticPastQueries:
    def __init__(self, index_name="past_queries"):
        self.index_name = index_name
        self.es = self.__get_es_instance()
        self.__create_index()

    def __get_es_instance(self):
        print("Connecting to Elasticsearch...")
        url = os.getenv("ELASTIC_URL")
        api_key = os.getenv("ELASTIC_PASSWORD")
        return Elasticsearch(
            url,
            basic_auth=("elastic", api_key),
            verify_certs=False
        )

    def index_document(self, document):
        response = self.es.index(index=self.index_name, document=document)
        return response

    def search_past_queries(self, query: str):
        multi_match_query = {
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["hypothesis", "query", "premises.premise", "premises.relationship", "premises.url", "premises.title", "premises.date"]
                }
            }
        }
        response = self.es.search(index=self.index_name, body=multi_match_query)

        results = [hit["_source"] for hit in response["hits"]["hits"]]

        return {
            "result": results
        }

    def __create_index(self):
        if not self.es.indices.exists(index=self.index_name):
            index_body = {
                "mappings": {
                    "properties": {
                        "hypothesis": {"type": "text"},
                        "query": {"type": "text"},
                        "premises": {
                            "type": "nested",
                            "properties": {
                                "premise": {"type": "text"},
                                "relationship": {"type": "text"},
                                "url": {"type": "text"},
                                "title": {"type": "text"},
                                "date": {"type": "text"}
                            }
                        }
                    }
                }
            }
            self.es.indices.create(index=self.index_name, body=index_body)
            print(f"Index '{self.index_name}' created.")
        else:
            print(f"Index '{self.index_name}' already exists.")