try to get it locally, if docker wont work. https://www.elastic.co/downloads/elasticsearch
CURRENT URL: https://localhost:9200 
(change upon deploy, or depending on your environment)
```
docker pull elasticsearch:8.15.2
```

```
docker network create es-network
```


```
docker run -d --name elasticsearch --net es-network -e "discovery.type=single-node" -e "ELASTIC_PASSWORD=mGgRy7ndsD7ozeTvv8hL" -p 9200:9200 -p 9300:9300 elasticsearch:8.15.2
```

see if the url work(localhost)
https://localhost:9200 

input:
```
user: elastic
password: mGgRy7ndsD7ozeTvv8hL
```