# How to run (Docker exclusive)
(Note: In order to run the coreference resolution, the project is running on python 3.7.10)

1. To run
```
docker-compose up
```


2. To stop 
```
docker-compose stop
```

You can optionally use the command below if you want the container deleted-not recommended
```
docker-compose down
```

Access using
[localhost:8000/](http://localhost:8000/)

or if it does not work
[127.0.0.1:8000](http://127.0.0.1:8000/)



#### This might be unstable since it is os/libraries versions dependent

3. To run with uvicorn(you can just run the last one, if you have ran the other commands before)
```
pip install -r requirements.txt

py download_nli.py

python -m spacy download en_core_web_sm

python -m uvicorn main:app --reload
```
access with: 
[127.0.0.1:8000](http://127.0.0.1:8000/)
