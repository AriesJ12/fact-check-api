from sumy.parsers.plaintext import PlaintextParser
from sumy.parsers.html import HtmlParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import nltk
import os
import requests
import random
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import Optional, List

class SummarizerService:
    class SummarizeRequest(BaseModel):
        data: List[Optional[str]]

    @staticmethod
    async def summarize(request: SummarizeRequest):
        method, language, sentence_count, input_type, input_, *rest = request.data
        
        if method == "LSA":
            from sumy.summarizers.lsa import LsaSummarizer as Summarizer
        elif method == "text-rank":
            from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer
        elif method == "lex-rank":
            from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer
        elif method == "edmundson":
            from sumy.summarizers.edmundson import EdmundsonSummarizer as Summarizer
        elif method == "luhn":
            from sumy.summarizers.luhn import LuhnSummarizer as Summarizer
        elif method == "kl-sum":
            from sumy.summarizers.kl import KLSummarizer as Summarizer
        elif method == "random":
            from sumy.summarizers.random import RandomSummarizer as Summarizer
        elif method == "reduction":
            from sumy.summarizers.reduction import ReductionSummarizer as Summarizer

        if input_type == "URL":
            parser = HtmlParser.from_url(input_, Tokenizer(language))
        elif input_type == "text":
            parser = PlaintextParser.from_string(input_, Tokenizer(language))

        stemmer = Stemmer(language)
        summarizer = Summarizer(stemmer)
        stop_words = get_stop_words(language)

        if method == "edmundson":
            summarizer.null_words = stop_words
            summarizer.bonus_words = parser.significant_words
            summarizer.stigma_words = parser.stigma_words
        else:
            summarizer.stop_words = stop_words

        summary_sentences = summarizer(parser.document, sentence_count)
        summary = " ".join([str(sentence) for sentence in summary_sentences])

        return summary