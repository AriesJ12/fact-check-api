from openai import OpenAI

from classes.Counter import Counter
class ClaimDetection:
    def __init__(self):
        pass
    
    @staticmethod
    def detect_claim(text):
        """returns yes or no"""
        counter_instance = Counter(db_file="gpt_calls.db", max_calls_per_day=80)
        counter_instance.update_counter()
        # client = OpenAI()
        # completion = client.chat.completions.create(
        #     model="gpt-4o-mini",
        #     messages=[
        #         {
        #             "role": "system",
        #             "content": "Classify the provided text as 'yes' or 'no' based on these rules:\n1. 'yes' if it's health-related and checkworthy.\n2. 'no' for all other cases."
        #         },
        #         {
        #             "role": "user",
        #             "content": text
        #         }
        #     ],
        #     temperature=0.2,
        #     max_tokens=64,
        #     top_p=0.1
        # )
        # return completion.choices[0].message.content
        return "yes"