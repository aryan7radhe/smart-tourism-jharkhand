import os 
from upstash_redis import Redis

redis = Redis(
    url = os.getenv("UPSTASH_REDIS_REST_URL"),
    token=os.getenv("UPSTASH_REDIS_REST_TOKEN")
)

def get_cache(key):
    try:
        return redis.get(key)
    except:
        return None
    

def set_cache(key,value,expire_seconds=3600):
    try:
        redis.set(key,value,ex=expire_seconds)
    except:
        pass
    