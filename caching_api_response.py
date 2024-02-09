import redis
import requests
import json

#Todo
#Read api data
#Cached fetchd data to redis
# Retrieve data from redis

redis_config = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'decode_responses': True
}

def read_api_data(char_id):
    response = requests.get("https://rickandmortyapi.com/api/character/" + str(char_id))
    data = response.json()
    return data

def cache_api_data(key,data,expire_in):
    r = redis.StrictRedis(**redis_config)
    r.set(key, json.dumps(data), ex=expire_in)

def read_cached_data(key):
    r = redis.StrictRedis(**redis_config)
    data = r.get(key)
    if data:
        return json.loads(data)
    else: return None

if __name__=='__main__':
    char_id = "2"
    
    cached_data = read_cached_data(char_id)
    if cached_data:
        print('Retrieving from cached data')
        print(cached_data)
    else:
        data = read_api_data(char_id)
        print('Retrieving from API')
        print(data)
        
        cache_api_data(char_id,data,60)