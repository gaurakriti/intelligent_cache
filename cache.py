import redis
import json

r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def get_cache(key):
    cached = r.get(key)
    return json.loads(cached) if cached else None

def set_cache(key, data, ttl=600):
    r.set(key, json.dumps(data), ex=ttl)
