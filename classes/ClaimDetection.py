from transformers import pipeline
class ClaimDetection:
    _instance = None
    _classifier = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ClaimDetection, cls).__new__(cls)
            cls._classifier = pipeline("zero-shot-classification", model="./nli")
        return cls._instance
    
    @staticmethod
    def detect_claim(text):
        """returns yes or no"""
        if ClaimDetection._classifier is None:
            ClaimDetection._classifier = pipeline("zero-shot-classification", model="./nli")
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
        
        