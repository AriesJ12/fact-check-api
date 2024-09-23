# from openai import OpenAI
import json
import os
from classes.Counter import Counter

import os
import google.generativeai as genai

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
        
        
        try:
            genai.configure(api_key=os.environ["GEMINI_API_KEY"])

            # Create the model
            generation_config = {
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 300,
                "response_mime_type": "application/json",
            }

            model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config=generation_config,
            system_instruction="You will be provided with a text. Identify up to 4 individual health-related claims and generate a separate, clear, and concise query for each claim. Respond with an array in the following format:\n[   \n{\n\"claim\": \"<individual health-related claim>\",\n\"query\": \"<clear and concise query>\"\n}\n]\nEnsure that:\n1. The response is only an array containing up to 4 objects.\n2. Each query corresponds to one health-related claim and does not combine multiple claims.\n3. The JSON output is complete and valid.\n4. Respond with the same language given to the text.\n5. If you did not find any health-related claims, respond with an empty array.",
            )

            chat_session = model.start_chat(
            history=[]
            )

            response = chat_session.send_message(text)
            # Extract the text content from the response
            response_text = response.candidates[0].content.parts[0].text
            # Parse the JSON response
            parsed_response = json.loads(response_text)
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

        # simulated_response = "[{\"claim\": \"Tea is associated with a lower risk of cognitive issues.\", \"query\": \"What is the evidence that tea consumption reduces the risk of cognitive issues?\"}, {\"claim\": \"Tea is associated with a lower risk of heart disease.\", \"query\": \"Is there a link between tea consumption and a lower risk of heart disease?\"}, {\"claim\": \"Tea is associated with a lower risk of stroke.\", \"query\": \"Does drinking tea reduce the risk of stroke?\"}, {\"claim\": \"Tea is associated with a lower risk of diabetes.\", \"query\": \"Is tea consumption associated with a lower risk of developing diabetes?\"}]\n"
        # parsed_response = json.loads(simulated_response)
        # return parsed_response
    
    
