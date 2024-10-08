from elasticsearch import Elasticsearch, helpers
import os
from dotenv import load_dotenv

load_dotenv()


class ElasticPastQueries:
    def __init__(self):
        self.index_name_bigqueries = "past_big_queries"
        self.index_name_smallqueries = "past_small_queries"
        self.es = self.__get_es_instance()
        self.__create_index_smallqueries()
        self.__create_index_bigqueries()

    def __get_es_instance(self):
        print("Connecting to Elasticsearch...")
        url = os.getenv("ELASTIC_URL")
        api_key = os.getenv("ELASTIC_PASSWORD")
        return Elasticsearch(
            url,
            basic_auth=("elastic", api_key),
            verify_certs=False
        )

    def index_document_bigqueries(self, document):
        response = self.es.index(index=self.index_name_bigqueries, document=document)
        return response

    def index_document_smallqueries(self, document):
        response = self.es.index(index=self.index_name_smallqueries, document=document)
        return response

    # 2. search all the past big queries
    def __search_whole_document_past_big_queries(self, bigquery, mode):
        index_name = self.index_name_bigqueries
        
        # Validate the mode
        if mode not in ["onlineDatabase", "google"]:
            raise ValueError("Invalid mode. Mode must be 'onlineDatabase' or 'google'.")

        # Construct the query with match_phrase
        query = {
            "bool": {
                "must": [
                    {"match_phrase": {"bigquery": bigquery}},  # Use match_phrase for phrase matching
                    {"term": {"mode": mode}}
                ]
            }
        }

        # Execute the search and limit results to 1
        response = self.es.search(index=index_name, query=query, size=1)

        # Check if any hits were returned
        if response["hits"]["total"]["value"] > 0:
            # Extract the top hit
            top_hit = response["hits"]["hits"][0]["_source"]
            # Validate that the bigquery matches
            if top_hit["bigquery"] == bigquery:
                return top_hit
            else:
                return None  # Or handle the mismatch as needed
        else:
            return None  # No matching document found

    def format_search_past_big_queries(self, bigquery, mode):
        # Retrieve the whole document based on the bigquery and mode
        document = self.__search_whole_document_past_big_queries(bigquery, mode)
        
        # If the document exists and has the "results" key, return only that
        if document and "results" in document:
            return document["results"]
        
        # If no matching document or "results" key is not present, return None
        return None

    # 3. search all the past results
    def search_past_results_only(self, search_query, mode):
        # Get results from both big and small queries indices
        big_results = self.__search_results_only_big_queries(search_query, mode)
        small_results = self.__search_results_only_small_queries(search_query, mode)

        # Combine the results from both indices
        combined_results = big_results + small_results

        return {"result": combined_results}

    # for small queries searching -- only returns the premises(used for retrieving past results before fact checking)
    def strict_search_past_results_only(self, search_query, mode):
        # Retrieve small results
        small_results = self.__search_results_only_small_queries(search_query, mode)

        # Check if there are results and take the top result
        if small_results:
            top_result = small_results[0]

            # Check if both hypothesis and query match the search_query
            if top_result.get("hypothesis") == search_query and top_result.get("query") == search_query:
                return top_result.get("premises", [])  # Return only premises if they match

        # Return None if no match is found
        return None

    def __search_results_only_big_queries(self, search_query, mode):
        index_name = self.index_name_bigqueries
        if mode not in ["onlineDatabase", "google"]:
            raise ValueError("Invalid mode. Mode must be 'onlineDatabase' or 'google'.")

        # Construct the search query with BM25 scoring
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"mode": mode}}  # Filter by mode
                    ],
                    "should": [
                        {
                            "nested": {
                                "path": "results",
                                "query": {
                                    "bool": {
                                        "should": [
                                            {"match": {"results.hypothesis": search_query}},  # BM25 match on hypothesis
                                            {"match": {"results.query": search_query}}       # BM25 match on query
                                        ]
                                    }
                                },
                                "inner_hits": {}  # Retrieve matching results within each document
                            }
                        }
                    ]
                }
            }
        }

        response = self.es.search(index=index_name, body=query)  # Use `body=query`
        results_only = []
        for hit in response["hits"]["hits"]:
            # Extract each matching `results` item from inner_hits
            for inner_hit in hit["inner_hits"]["results"]["hits"]["hits"]:
                # Structure each result with hypothesis, query, and premises
                result_entry = {
                    "hypothesis": inner_hit["_source"].get("hypothesis", ""),
                    "query": inner_hit["_source"].get("query", ""),
                    "premises": inner_hit["_source"]["premises"]
                }
                results_only.append(result_entry)

        return results_only

    def __search_results_only_small_queries(self, search_query, mode):
        index_name = self.index_name_smallqueries

        # Construct the search query with BM25 scoring
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"mode": mode}}  # Filter documents by mode
                    ],
                    "should": [
                        {"match": {"hypothesis": search_query}},  # BM25 match on hypothesis
                        {"match": {"query": search_query}}       # BM25 match on query
                    ]
                }
            }
        }

        response = self.es.search(index=index_name, body=query)
        results_only = []
        for hit in response["hits"]["hits"]:
            # Structure each result with hypothesis, query, and premises
            result_entry = {
                "hypothesis": hit["_source"].get("hypothesis", ""),
                "query": hit["_source"].get("query", ""),
                "premises": hit["_source"]["premises"]
            }
            results_only.append(result_entry)
        return results_only

    def __create_index_smallqueries(self, index_name="past_small_queries"):
        settings = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0,
                "analysis": {
                    "analyzer": {
                        "default": {
                            "type": "standard"
                        }
                    }
                }
            },
            "mappings": {
                "properties": {
                    "hypothesis": {"type": "text"},
                    "query": {"type": "text"},
                    "mode": {
                        "type": "keyword",
                    },
                    "premises": {
                        "type": "nested",
                        "properties": {
                            "premise": {"type": "text"},
                            "relationship": {"type": "keyword"},
                            "url": {"type": "keyword"},
                            "title": {"type": "text"},
                            "date": {"type": "text"}
                        }
                    }
                }
            }
        }
        if not self.es.indices.exists(index=index_name):
            self.es.indices.create(index=index_name, body=settings)
            print(f"Index {index_name} created with mode restriction")
        else:
            print(f"Index {index_name} already exists")
        pass

    def __create_index_bigqueries(self, index_name="past_big_queries"):
        # change settings when deploying
        settings = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0,
                "analysis": {
                    "analyzer": {
                        "default": {
                            "type": "standard"
                        }
                    }
                }
            },
            "mappings": {
                "properties": {
                    "bigquery": {"type": "text"},
                    "mode": {
                        "type": "keyword",
                    },
                    "results": {
                        "type": "nested",
                        "properties": {
                            "hypothesis": {"type": "text"},
                            "query": {"type": "text"},
                            "premises": {
                                "type": "nested",
                                "properties": {
                                    "premise": {"type": "text"},
                                    "relationship": {"type": "keyword"},
                                    "url": {"type": "keyword"},
                                    "title": {"type": "text"},
                                    "date": {"type": "text"}
                                }
                            }
                        }
                    }
                }
            }
        }
        if not self.es.indices.exists(index=index_name):
            self.es.indices.create(index=index_name, body=settings)
            print(f"Index {index_name} created with mode restriction")
        else:
            print(f"Index {index_name} already exists")