from .NLISingleton import NLISingleton
import torch

class Premise:
    def __init__(self, hypothesis):
        # Ensure the model is initialized
        NLISingleton()  # This line ensures the model is initialized
        self.hypothesis = hypothesis
        self.premises = []
        self.relationship = []
    
    def add_premise(self, premise, url, title, date):
        temp_premise = {
            'premise': premise,
            'url': url,
            'title': title,
            'date': date
        }
        self.premises.append(temp_premise)

    def determine_all_relationship_premise_hypothesis(self):
        if not self.premises:
            return
        tokenizer = NLISingleton.get_tokenizer()
        model = NLISingleton.get_model()
        device = NLISingleton.get_device()
    
        hypothesis = self.hypothesis
        premises = [premise['premise'] for premise in self.premises]
    
        hypotheses = [hypothesis] * len(premises)
        inputs = tokenizer(premises, hypotheses, return_tensors='pt', padding=True, truncation=True)
    
        # Move inputs to the device (CPU)
        inputs = {key: value.to(device) for key, value in inputs.items()}
    
        # Run batch inference
        with torch.no_grad():  # Disable gradient calculation for inference
            outputs = model(**inputs)
    
        # Get logits and apply softmax
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=-1)
    
        # Label mapping for NLI
        label_names = ["entailment", "neutral", "contradiction"]
    
        for i, probs in enumerate(probabilities):
            label_idx = torch.argmax(probs).item()
            self.premises[i]['relationship'] = label_names[label_idx]
        
    def get_all_premises_with_relationship(self):
        return self.premises
