from .NLISingleton import NLISingleton
import torch

class Premise:
    def __init__(self, premise, hypothesis, url, title, date):
        # Ensure the model is initialized
        NLISingleton()  # This line ensures the model is initialized
        self.premise = premise
        self.url = url
        self.title = title
        self.date = date
        self.relationship = self.__determine_relationship_premise_hypothesis(premise, hypothesis)
    
    def __determine_relationship_premise_hypothesis(self, premise, hypothesis):
        model = NLISingleton.get_model()
        tokenizer = NLISingleton.get_tokenizer()
        device = NLISingleton.get_device()

        input = tokenizer(premise, hypothesis, truncation=True, return_tensors="pt")
        output = model(input["input_ids"].to(device))  # device = "cuda:0" or "cpu"
        prediction = torch.softmax(output["logits"][0], -1).tolist()
        label_names = ["entailment", "neutral", "contradiction"]
        prediction_dict = {name: round(float(pred) * 100, 1) for pred, name in zip(prediction, label_names)}

        # Get the label with the highest probability
        highest_label = max(prediction_dict, key=prediction_dict.get)

        return highest_label

    def to_json(self):
        return {
            'premise': self.premise,
            'relationship': self.relationship,
            'url': self.url,
            'title': self.title,
            'date': self.date
        }
