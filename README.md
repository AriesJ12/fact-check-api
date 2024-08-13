# How to run (Docker exclusive) -- recommended if you want to deploy in a server or if the fast api doesnt work in your pc

- prerequisite:
download the pytorch_model.bin in https://huggingface.co/ctu-aic/xlm-roberta-large-squad2-ctkfacts_nli/tree/main
put it in the nli folder

Python version: 3.12.4
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



# recommended if you are trying to install in your pc only; This might be unstable since it is os/libraries versions dependent

3. To run with uvicorn(you can just run the last one, if you have ran the other commands before)
```
pip install -r requirements.txt

py download_nli.py

python -m uvicorn main:app --reload
```
access with: 
[127.0.0.1:8000](http://127.0.0.1:8000/)
