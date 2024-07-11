import torch

from .NLISingleton import NLISingleton


class Premise:
    def __init__(self, premise, hypothesis, url):
        # Ensure the model is initialized
        NLISingleton(model_path='../nli')  # This line ensures the model is initialized
        self.premise = premise
        self.url = url
        self.relationship = self._determine_relationship_premise_hypothesis(premise, hypothesis)
    
    def _determine_relationship_premise_hypothesis(self, premise, hypothesis):
        model = NLISingleton.get_model()
        text_pairs = [[premise, hypothesis]]
        logits = model.predict(text_pairs)

        # Apply softmax to convert logits to probabilities
        probabilities = torch.nn.functional.softmax(torch.tensor(logits), dim=-1).numpy()

        # Get the index of the highest probability
        prediction = probabilities.argmax()

        # Map index to label
        labels = ["entailment", "neutral", "contradiction"]
        predicted_label = labels[prediction]

        return predicted_label

    def to_json(self):
        return {
            'premise': self.premise,
            'relationship': self.relationship,
            'url': self.url
        }
