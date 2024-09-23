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
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            system_instruction="""
            You will be given a text. Identify up to 4 individual health-related claims within the text and generate a separate, clear, and concise query for each claim. Respond with an array in the following format:
                [   
                { 
                    \"claim\": \"<individual health-related claim>\",
                    \"query\": \"<clear and concise query>\"
                }
                ]
                Ensure that:
                1. The response is only an array containing up to 4 objects, each representing one distinct health-related claim.
                2. Each query directly addresses the corresponding health-related claim and does not combine multiple claims.
                3. The JSON output is valid and complete.
                4. Respond in the same language as the provided text.
                5. If no health-related claims are found or fewer than four exist, respond with an array containing only the identified claims or an empty array if none are found."
            """
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
    
    
