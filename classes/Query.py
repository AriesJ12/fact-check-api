from openai import OpenAI
import json
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
            },

        ]
        
        """
        # client = OpenAI()
        # completion = client.chat.completions.create(
        #     model="gpt-4o-mini",
        #     messages=[
        #         {
        #             "role": "system",
        #             "content": """
        #                 You will be provided with a text. Identify each individual health-related claim and generate a separate, clear, and concise query for each claim. Respond with an array in the following format:
        #                 [   
        #                     {
        #                         "claim": "<individual health-related claim>",
        #                         "query": "<clear and concise query>"
        #                     }
        #                 ]
        #                 Ensure that the response is only an array. And each query corresponds to one health-related claim and does not combine multiple claims.
        #                 You will be provided with text in various languages. Always respond in English, regardless of the language of the input text.
        #             """
        #         },
        #         {
        #             "role": "user",
        #             "content": text
        #         }
        #     ],
        #     temperature=0.3,
        #     top_p=0.2
        # )
        # parsed_response = json.loads(completion.choices[0].message.content)
        sample_response = """
        [
            {
                "claim": "Covid is deadly",
                "query": "Covid is deadly"
            },
            {
                "claim": "Polio is deadly",
                "query": "Polio is deadly"
            }
        ]
        """
        parsed_response = json.loads(sample_response)
        return parsed_response
    
