
from .SpacyModelSingleton import SpacyModelSingleton

from .Translate import Translate

class Query:
    def __init__(self, query):
        self.nlp = SpacyModelSingleton.get_instance('en_core_web_sm')
        self.query = query
        self.dividedQueries = self._query_builder(query)

    # Sentence segmentation and coreference resolution(eg. "it" refers to "the dog" in "The dog ran. It was fast.")
    def _sentence_segmentation_with_coref(self, text):
        """
        Segments the given text into sentences with optional co-reference resolution.
        
        Args:
            text (str): The input text to process.
        
        Returns:
            List[str]: A list of sentences from the potentially co-reference resolved text.
        """
        # Check and add NeuralCoref to the pipeline if not already present
        
        # Process the text with Spacy's pipeline, including NeuralCoref
        doc = self.nlp(text)
        
        # Resolve co-references if present, else use original text
        resolved_text = doc._.coref_resolved if doc._.has_coref else text
        
        # Re-process the resolved text for sentence segmentation
        sentences = [sent.text.strip() for sent in self.nlp(resolved_text).sents]
        
        return sentences
    
    def _query_builder(self, text):
        return text.split(".")
        # Process the text with spaCy to create a Doc object
        doc = self.nlp(text)
        # Count the sentences by iterating over Doc.sents
        sentence_count = len(list(doc.sents))
        
        if sentence_count <= 2:
            # Directly check if the text (1 or 2 sentences) is a claim
            is_claim = self._claim_detection([text])
            processed_sentences = [text]
            # if is_claim:  # Assuming _claim_detection returns a boolean or similar for claim detection
            #     processed_sentences = [self._remove_stopwords(text)]
            # else:
            #     processed_sentences = []
        else:
            sentences = self._sentence_segmentation_with_coref(text)
            # Perform claim detection on each sentence
            claims = self._claim_detection(sentences)
            # Remove stopwords from sentences identified as claims
            # processed_sentences = [self._remove_stopwords(sentence) for sentence, is_claim in zip(sentences, claims) if is_claim]
            processed_sentences = sentences

        return processed_sentences
    
    # llama api url --- might not be needed
    @staticmethod
    def _query(prompt):
        API_URL = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
        token = os.getenv("HUGGING_FACE_TOKEN")
        headers = {"Authorization": f"Bearer {token}"}

        payload = {
            "inputs": prompt,
            "parameters" :{
                "return_full_text": False,
                "num_return_sequences": 1
            }
        }

        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    def _translate_to_english(self, text):
        # # URL where the LibreTranslate API is accessible
        # libretranslate_url = "http://localhost:5000/translate"
        
        # # Prepare the data for the POST request
        # data = {
        #     "q": text,
        #     "source": "auto",  # Let LibreTranslate detect the source language
        #     "target": "en",    # Target language is English
        #     "format": "text"
        # }
        
        # # Send the request to the LibreTranslate API
        # try:
        #     response = requests.post(libretranslate_url, data=data)
        #     response.raise_for_status()  # Raises an error for bad responses
        #     return response.json()['translatedText']
        # except requests.RequestException as e:
        #     print(f"Request failed: {e}")
        #     return None
        return text

    def _remove_stopwords(self, text):
        try:
            stopwords = set(stopwords.words('english'))
        except:
            nltk.download('stopwords')
            stopwords = set(stopwords.words('english'))
        
        word_tokens = word_tokenize(text)
        filtered_text = [word for word in word_tokens if word.lower() not in stopwords]
        return " ".join(filtered_text)

    def _claim_detection(self, texts):
        API_URL = "https://api-inference.huggingface.co/models/Nithiwat/xlm-roberta-base_claim-detection"
        token = os.getenv("HUGGING_FACE_TOKEN")
        headers = {"Authorization": f"Bearer {token}"}

        def query(payload):
            response = requests.post(API_URL, headers=headers, json=payload)
            return response.json()
            
        outputs = query({
            "inputs": texts,
        })
        return outputs

    def _retained_check_worth(self, text):
        pass

    def get_divided_queries(self):
        return self.dividedQueries
