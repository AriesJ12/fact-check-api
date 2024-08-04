from classes.ClaimDetection import ClaimDetection
from classes.FactCheck import FactCheckResult
from classes.Query import Query

def main_fact_check(text):
    """expected result:
        const sampleFact = {
        result: [
          {
            hypothesis: 'sample',
            premises: [
              {
                premise: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec odio.',
                relationship: 'contradiction',
                url: 'https://example.com',
                title: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec odio.',
                date: ""
              },
              {
                premise: '2',
                relationship: 'entailment',
                url: 'https://example.com',
                title: 'Some other title',
                date: ""
              },
              {
                premise: '3',
                relationship: 'neutral',
                url: 'https://example.com',
                title: 'Some 123 title',
                date: ""
              },
              {
                premise: '4',
                relationship: 'neutral',
                url: 'https://example.com',
                title: 'Some 333 title',
                date: ""
              },
            ],
          },
          {
            hypothesis: 'sample ',
            premises: [
              {
                premise: '1',
                relationship: 'contradiction',
                url: 'https://example.com',
                title: 'Some title',
                date: "3/4/2021"
              },
              {
                premise: '2',
                relationship: 'entailment',
                url: 'https://example.com',
                title: 'Some title',
                date: "3/4/2121"
              },
              {
                premise: '3',
                relationship: 'neutral',
                url: 'https://example.com',
                title: 'Some title',
                date: "33/3/333"
              },
            ],
          },
          {
            hypothesis: '100000',
            premises: [
              {
                premise: '1',
                relationship: 'contradiction',
                url: 'https://example.com',
                title: 'Some title',
                date: ""
              },
              {
                premise: '2',
                relationship: 'entailment',
                url: 'https://example.com',
                title: 'Some title',
                date: ""
              },
              {
                premise: '3',
                relationship: 'neutral',
                url: 'https://example.com',
                title: 'Some title',
                date: ""
              },
            ],
          },
        ],
      };

    """
    
  
    claimsPairs = Query.query_builder(text)
    # return claims
    
    maxClaimsToCheck = 5
    FactCheckResultJson = []
    
    for i in range(min(maxClaimsToCheck, len(claimsPairs))):
        query = claimsPairs[i]['query']
        claim = claimsPairs[i]['claim']
        factClass = FactCheckResult(query=query, hypothesis=claim)
        factClass.get_All_Premises()
        FactCheckResultJson.append(factClass.to_json())
    # return the list of FactCheckResult objects
    
    return {"result": FactCheckResultJson}


def main_fact_check_without_query(text):
    """expected result:
    [
        {
            premise: '1',
            relationship: 'contradiction',
            url: 'https://example.com',
            title: 'Some title',
            date: ""
        },
        {
            premise: '2',
            relationship: 'entailment',
            url: 'https://example.com',
            title: 'Some title',
            date: ""
        },
        {
            premise: '3',
            relationship: 'neutral',
            url: 'https://example.com',
            title: 'Some title',
            date: "3232"
        },
        {
            premise: '4',
            relationship: 'neutral',
            url: 'https://example.com',
            title: 'Some title',
            date: ""
        },
    ];
    """
    factClass = FactCheckResult(text)
    factClass.get_All_Premises()
    return factClass.get_processed_premises

    

def main_claim_detection(text):
    """expected result:
        {"result" : "yes"} or {"result" : "no"}
    """
    result = ClaimDetection.detect_claim(text)
    if result == "no" or result == "yes":
        return {"result" : result}
    else:
        return {"result" : "error"}