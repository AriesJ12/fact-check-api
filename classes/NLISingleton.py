from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class NLISingleton:
    _instance = None
    _model = None
    _tokenizer = None
    _device = None

    def __new__(cls, model_path='./nli'):
        if cls._instance is None:
            cls._instance = super(NLISingleton, cls).__new__(cls)
            # Ensure the model is correctly loaded here
            cls._model = AutoModelForSequenceClassification.from_pretrained(model_path)
            cls._tokenizer = AutoTokenizer.from_pretrained(model_path)
            cls._device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        return cls._instance

    @classmethod
    def get_model(cls, model_path='./nli'):
        # Ensure _model is not None before returning it
        if cls._model is None:
            AutoModelForSequenceClassification.from_pretrained(model_path)
        return cls._model
    
    @classmethod
    def get_tokenizer(cls, model_path='./nli'):
        if cls._tokenizer is None:
            AutoTokenizer.from_pretrained(model_path)
        return cls._tokenizer
    
    @classmethod
    def get_device(cls):
        if cls._device is None:
            cls._device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
        return cls._device