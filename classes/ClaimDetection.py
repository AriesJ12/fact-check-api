from transformers import pipeline
from classes.Counter import Counter
import torch
class ClaimDetection:
    _instance = None
    _classifier = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ClaimDetection, cls).__new__(cls)
            device = 0 if torch.cuda.is_available() else -1
            cls._classifier = pipeline("zero-shot-classification", model="./nli", device=device)
        return cls._instance
    

    @staticmethod
    def detect_claim(text):
        # added this so that the number of calls per day does not exceed alot for backend deployment
        counter_instance = Counter(db_file="gpt_calls.db", max_calls_per_day=120)
        counter_instance.update_counter()
        """returns yes or no"""
        if ClaimDetection._classifier is None:
            device = 0 if torch.cuda.is_available() else -1
            ClaimDetection._classifier = pipeline("zero-shot-classification", model="./nli", device=device)
        # Define the text to classify and candidate labels
        sequence_to_classify = text
        candidate_labels = ["health", "non-health"]

        # Perform the classification
        output = ClaimDetection._classifier(sequence_to_classify, candidate_labels, multi_label=False)

        # Extract the label with the highest score
        highest_score_label = output['labels'][0]

        # Determine if the highest scoring label is 'health'
        if highest_score_label == "health":
            result = "yes"
        else:
            result = "no"

        return result
        
        