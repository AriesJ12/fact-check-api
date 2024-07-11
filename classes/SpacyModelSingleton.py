import spacy
import neuralcoref


class SpacyModelSingleton:
    _instance = None

    @classmethod
    def get_instance(cls, model_name='en_core_web_sm'):
        if cls._instance is None:
            print(f"Loading Spacy model {model_name} and adding neuralcoref...")
            # Load the Spacy model with the given model name
            nlp = spacy.load(model_name)
            # Add neuralcoref to it
            neuralcoref.add_to_pipe(nlp)
            cls._instance = nlp
        return cls._instance
    