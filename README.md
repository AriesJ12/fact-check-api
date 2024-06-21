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


4. run server api
```
python -m uvicorn main:app --reload
```

