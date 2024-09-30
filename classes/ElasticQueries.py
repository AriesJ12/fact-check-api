from elasticsearch import Elasticsearch, helpers
import os
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModel
import torch
import torch.nn.functional as F

load_dotenv()

class ElasticQueries:
    # Class-level variables for singleton instances
    __tokenizer = None
    __model = None
    __es_instance = None
    __index_created = False  # To track index creation
    __index_name = "past_queries"

    def __init__(self, index_name="past_queries"):
        self.index_name = index_name
        self.es = self.__get_es_instance()
        self.tokenizer = self.__get_tokenizer()
        self.model = self.__get_model()
        
        # Create index only once when the server starts
        if not self.__index_created:
            self.__create_index()
            ElasticQueries.__index_created = True  # Set the flag to True after creation

    @classmethod
    def __get_tokenizer(cls):
        if cls.__tokenizer is None:
            print("Loading tokenizer...")
            cls.__tokenizer = AutoTokenizer.from_pretrained('./semantic_model')  # Load from local directory
        return cls.__tokenizer

    @classmethod
    def __get_model(cls):
        if cls.__model is None:
            print("Loading model...")
            cls.__model = AutoModel.from_pretrained('./semantic_model')  # Load from local directory
            cls.__model.eval()  # Set the model to evaluation mode
        return cls.__model

    @classmethod
    def __get_es_instance(cls):
        if cls.__es_instance is None:
            print("Connecting to Elasticsearch...")
            url = os.getenv("ELASTIC_URL")
            api_key = os.getenv("ELASTIC_PASSWORD")
            cls.__es_instance = Elasticsearch(
                url,
                basic_auth=("elastic", api_key),
                verify_certs=False
            )
        return cls.__es_instance

    def __generate_embedding(self, text):
        text_for_embedding = "query: " + text
        inputs = self.tokenizer(text_for_embedding, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
        embeddings = self.__average_pool(outputs.last_hidden_state, inputs['attention_mask'])
        embeddings = F.normalize(embeddings, p=2, dim=1)
        return embeddings.squeeze().tolist()

    def __average_pool(self, last_hidden_states, attention_mask):
        last_hidden = last_hidden_states.masked_fill(~attention_mask[..., None].bool(), 0.0)
        return last_hidden.sum(dim=1) / attention_mask.sum(dim=1)[..., None]

    def index_document(self, document):
        embedding = self.__generate_embedding(document['query'])
        document['query_vector'] = embedding
        
        response = self.es.index(index=self.index_name, document=document)
        return response

    def search_past_queries(self, query: str):
        query_embedding = self.__generate_embedding(query)

        sem_query = {
            "knn": {
                "field": "query_vector",
                "query_vector": query_embedding,
                "k": 10,
                "num_candidates": 25
            }
        }
        sem_response = self.es.search(index=self.index_name, body=sem_query)

        sem_results = [hit["_source"] for hit in sem_response["hits"]["hits"]]

        return {
            "result": sem_results
        }

    @classmethod
    def __create_index(cls):
        if not cls.__es_instance.indices.exists(index=cls.__index_name):
            index_body = {
                "mappings": {
                    "properties": {
                        "hypothesis": {"type": "text"},
                        "query": {"type": "text"},
                        "query_vector": {"type": "dense_vector", "dims": 384, "index": True, "similarity": "cosine"},
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
            cls.__es_instance.indices.create(index=cls.__index_name, body=index_body)
            print(f"Index '{cls.__index_name}' created.")
        else:
            print(f"Index '{cls.__index_name}' already exists.")
