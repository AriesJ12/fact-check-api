from openai import OpenAI
import json
import os
from classes.Counter import Counter

class Query:
    def __init__(self, query):
        pass

    @staticmethod
    def query_builder(text):
        """returns:
        [
            {
                "claim": "<individual health-related claim>",
                "query": "<clear and concise query>"
            },
            {
                "claim": "<individual health-related claim>",
                "query": "<clear and concise query>"
            }
        ]
        
        """
        counter_instance = Counter(db_file="gpt_calls.db", max_calls_per_day=80)
        counter_instance.update_counter()
        
        deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        if not deepseek_api_key:
            raise ValueError("Error accessing backend API")
        
        try:
            client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")
            completion = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {
                        "role": "system",
                        "content": """
                            You will be provided with a text. Identify up to 4 individual health-related claims and generate a separate, clear, and concise query for each claim. Respond with an array in the following format:
                                [   
                                    {
                                        "claim": "<individual health-related claim>",
                                        "query": "<clear and concise query>"
                                    }
                                ]
                                Ensure that:
                                1. The response is only an array containing up to 4 objects.
                                2. Each query corresponds to one health-related claim and does not combine multiple claims.
                                3. The JSON output is complete and valid.
                                4. Respond with the same language given to the text.
                                5. If you did not find any health-related claims, respond with an empty array.
                            """
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                temperature=1.0,
                stream=False
            )
            parsed_response = json.loads(completion.choices[0].message.content)
            return parsed_response
        except Exception as e:
            raise Exception("Error accessing backend API")
        
        
        # json_response = f"""
        #     [
        #         {{
        #             "claim": "{text}",
        #             "query": "{text}"
        #         }}
        #     ]
        #     """
        # parsed_response = json.loads(json_response)
        # return parsed_response
    
    
