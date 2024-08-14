import tiktoken

class TokenCounter:
    def __init__(self, ):
        pass
    
    @staticmethod
    def is_in_range_text(text, max_tokens):
        MODEL_NAME='cl100k_base'
        TOKENIZER = tiktoken.get_encoding(MODEL_NAME)
        tokens = TOKENIZER.encode(text)

        total_tokens = len(tokens)
        return total_tokens <= max_tokens