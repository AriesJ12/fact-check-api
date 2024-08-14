from classes.ClaimDetection import ClaimDetection
from classes.FactCheck import FactCheckResult
from classes.Query import Query
from classes.TokenCounter import TokenCounter


"""
returns:
expected result,
{result: Invalid number of tokens},
{result: Daily limit reached},
{result: error} 
"""
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
    
    MAX_TOKENS = 150
    is_in_range_token = TokenCounter.is_in_range_text(text=text, max_tokens=MAX_TOKENS)
    if (not is_in_range_token):
        return {"result" : "Invalid number of tokens"}
    try:
      claimsPairs = Query.query_builder(text)
    except Exception as e:
      print(e)
      return {"result" : str(e)}
    maxClaimsToCheck = 5
    FactCheckResultJson = []
    
    for i in range(min(maxClaimsToCheck, len(claimsPairs))):
        query = claimsPairs[i]['query']
        claim = claimsPairs[i]['claim']
        factClass = FactCheckResult(query=query, hypothesis=claim)
        try:
          factClass.get_All_Premises()
        except Exception as e:
          print(e)
          return {"result" : str(e)}
        FactCheckResultJson.append(factClass.to_json())
    # return the list of FactCheckResult objects
    
    return {"result": FactCheckResultJson}


"""
returns:
expected result,
{result: Invalid number of tokens},
{result: No claim detected},
{result: Daily limit reached},
{result: error} 
"""
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
    
    # check max tokens
    MAX_TOKENS = 50
    is_in_range_token = TokenCounter.is_in_range_text(text=text, max_tokens=MAX_TOKENS)
    if (not is_in_range_token):
        return {"result" : "Invalid number of tokens"}
    
    # check if its a claim
    is_health_claim = ClaimDetection.detect_claim(text)
    if is_health_claim == "no":
        return {"result" : "No claim detected"}
    if not is_health_claim == "yes":
        return {"result" : "error"}

    factClass = FactCheckResult(query=text, hypothesis=text)
    try:
      factClass.get_All_Premises()
    except Exception as e:
      print(e)
      return {"result" : str(e)}
    return factClass.get_processed_premises()


"""
returns:
expected result,
{result: Invalid number of tokens},
{result: error} 
"""
def main_claim_detection(text):
    """expected result:
        {"result" : "yes"} or {"result" : "no"}
    """
    # Check tokens
    MAX_TOKENS = 100
    is_in_range_token = TokenCounter.is_in_range_text(text=text, max_tokens=MAX_TOKENS)
    if (not is_in_range_token):
        return {"result" : "Invalid number of tokens"}
    
    try:
      result = ClaimDetection.detect_claim(text)
    except Exception as e:
      print(e)
      return {"result" : str(e)}
    
    if result == "no" or result == "yes":
        return {"result" : result}
    else:
        return {"result" : "error"}
    

# if __name__ == '__main__':
#     text = "Covid is deadly"
#     print(main_claim_detection(text))
    # print(main_fact_check_without_query(text))
#     print(main_fact_check(text))
