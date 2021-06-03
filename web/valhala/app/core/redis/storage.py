# redis stuff
from redis import Redis

redis_client = Redis(host="0.0.0.0", port=6379)

class RedisStorage:
    def __init__(self):
        self.storage = redis_client

    def getValue(self, key: str):
        return self.storage.get(key)

    def setValue(self, key: str, value):
        self.storage.set(key, value)

    def setEx(self, key: str, time, value):
        self.storage.setex(key, time, value)
    
    def rpush(self, key: str, value):
        self.storage.rpush(key, value)