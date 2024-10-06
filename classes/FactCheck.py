from .Premise import Premise
from .SearchDatabase import SearchDatabase
class FactCheckResult:
    def __init__(self, query, hypothesis, mode):
        self.query = query
        self.hypothesis = hypothesis
        self.premiseClass = Premise(hypothesis=hypothesis)
        self.mode = mode
    
    def __add_premise(self, premise, url, title, date):
        self.premiseClass.add_premise(premise=premise, url=url, title=title, date=date)

    def get_All_Premises(self):
        query = self.query
        search = SearchDatabase(query=query, mode=self.mode)
        results = search.get_results()
        init_premises = 0
        MAX_PREMISES = 10

        for item in results:
            if init_premises >= MAX_PREMISES:
                break

            url = item.get("url", "No URL available")
            title = item.get("title", "No title available")
            date = item.get("date", "No date available")
            snippets = item["premise"]

            if snippets:
                for snippet in snippets:
                    if snippet.strip():
                        self.__add_premise(premise=snippet, url=url, title=title, date=date)
                        init_premises += 1
                        if init_premises >= MAX_PREMISES:
                            break

        self.premiseClass.determine_all_relationship_premise_hypothesis()

    def to_json(self):
        return {
            'hypothesis': self.hypothesis,
            'premises': self.premiseClass.get_all_premises_with_relationship()
        }
    
    def get_processed_premises(self):
        return self.premiseClass.get_all_premises_with_relationship() #change here

