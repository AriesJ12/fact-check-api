from .NLISingleton import NLISingleton


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
        scores = model.predict([(premise, hypothesis)])

        label_mapping = ['contradiction', 'entailment', 'neutral']
        labels = [label_mapping[score_max] for score_max in scores.argmax(axis=1)]
        predicted_label = labels[0]

        return predicted_label

    def to_json(self):
        return {
            'premise': self.premise,
            'relationship': self.relationship,
            'url': self.url,
            'title': self.title,
            'date': self.date
        }
