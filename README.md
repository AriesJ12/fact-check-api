# How to run (Docker exclusive)
1. 

# fact-check-api

1. copy ".env example" renamed to env and fill up the values


2. install dependencies:

```
pip install -r requirements.txt
```

3. Download the nli model necessary:
```
py download_nli.py
```
4. Download spacy en_core_web(You might get an error while doing this step, make sure to download the latest microsoft c++ redistributable)
```
python -m spacy download en_core_web_sm
```


5. run server api
```
python -m uvicorn main:app --reload
```

