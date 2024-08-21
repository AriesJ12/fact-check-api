- prerequisite:
download the model.safetensors in https://huggingface.co/MoritzLaurer/mDeBERTa-v3-base-xnli-multilingual-nli-2mil7/tree/main
put it in the nli folder

# run with docker


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
docker-compose down --rmi all
```

Access using
[localhost:8000/](http://localhost:8000/)

or if it does not work
[127.0.0.1:8000](http://127.0.0.1:8000/)



# without docker

3. To run with uvicorn(you can just run the last one, if you have ran the other commands before)
```
pip install -r requirements.txt

python -m uvicorn main:app --reload
```
access with: 
[127.0.0.1:8000](http://127.0.0.1:8000/)
