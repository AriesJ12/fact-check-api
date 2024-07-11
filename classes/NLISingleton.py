from sentence_transformers.cross_encoder import CrossEncoder

class NLISingleton:
    _instance = None
    _model = None

    def __new__(cls, model_path='./nli'):
        if cls._instance is None:
            cls._instance = super(NLISingleton, cls).__new__(cls)
            # Ensure the model is correctly loaded here
            cls._model = CrossEncoder(model_path)
        return cls._instance

    @classmethod
    def get_model(cls, model_path='./nli'):
        # Ensure _model is not None before returning it
        if cls._model is None:
            cls._model = CrossEncoder(model_path)
        return cls._model