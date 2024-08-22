from openai import OpenAI
import json

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
        # client = OpenAI()
        # completion = client.chat.completions.create(
        #     model="gpt-4o-mini",
        #     messages=[
        #         {
        #             "role": "system",
        #             "content": """
                    #    You will be provided with a text. Identify up to 4 individual health-related claims and generate a separate, clear, and concise query for each claim. Respond with an array in the following format:
                    #     [   
                    #         {
                    #             "claim": "<individual health-related claim>",
                    #             "query": "<clear and concise query>"
                    #         }
                    #     ]
                    #     Ensure that:
                    #     1. The response is only an array containing up to 4 objects.
                    #     2. Each query corresponds to one health-related claim and does not combine multiple claims.
                    #     3. The JSON output is complete and valid.
                    #     4. Always respond in English, regardless of the language of the input text.
                    #     5. If you did not find any health-related claims, respond with an empty array.
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
        if("Polio is a highly infectious disease caused by a virus. It invades the nervous system and can cause total paralysis in a matter of hours" == text):
            sample_response = """
            [
                {
                    "claim": "Polio is a highly infectious disease caused by a virus.",
                    "query": "Is polio a highly infectious disease caused by a virus?"
                },
                {
                    "claim": "Polio invades the nervous system.",
                    "query": "Does polio invade the nervous system?"
                },
                {
                    "claim": "Polio can cause total paralysis in a matter of hours.",
                    "query": "Can polio cause total paralysis in a matter of hours?"
                }
            ]
            """
        else:
            sample_response = """
            [
    {
        "claim": "Poor sleep leads to weight gain.",
        "query": "Does poor sleep lead to weight gain?"
    },
    {
        "claim": "Poor sleep weakens the immune system.",
        "query": "Does poor sleep weaken the immune system?"
    },
    {
        "claim": "Poor sleep negatively affects heart health.",
        "query": "Does poor sleep negatively affect heart health?"
    },
    {
        "claim": "Poor sleep leads to higher blood pressure.",
        "query": "Does poor sleep lead to higher blood pressure?"
    }
]
            """
        parsed_response = json.loads(sample_response)
        return parsed_response
    
    
