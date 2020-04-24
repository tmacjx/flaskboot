"""
# @Author  wk
# @Time 2020/4/23 18:37

"""
import redis_sentinel_url
from app import config
import logging


def create_redis_connection():
    logging.debug("Creating Redis connection (%s)", config.REDIS_URL)
    max_connections = config.REDIS_POOL_SIZE
    client_options = {"retry_on_timeout": True, "decode_responses": True,
                      "socket_keepalive": True, "max_connections": max_connections}

    sentinel, client = redis_sentinel_url.connect(config.REDIS_URL, client_options=client_options)
    return client


class RedisClient(object):
    def __init__(self, client):
        self._client = client

    def lua_lock(self):
        pass

    def setnx(self, name, value, time=None):
        """
        :param name:
        :param value:
        :param time:
        :return:
        """
        lua_script = """
           local n = redis.call('setnx', KEYS[1], ARGV[1])
           if n == 1
               then redis.call('expire', KEYS[1], ARGV[2])
               end
           return n
           """
        res = self._client.register_script(lua_script)(keys=[name], args=[value, time])
        return res

    def inc(self, key, step, time):
        """
        :return:
        """
        lua_script = """
            local n = redis.call('setnx', KEYS[1], 0)" 
            if n == 1 
                then redis.call('expire', KEYS[1], ARGV[2])
                n = redis.call('INCRBY', KEYS[1], ARGV[1])
            else
                 n=redis.call('INCRBY', KEYS[1], ARGV[1])
                 end
            return n"""
        res = self._client.register_script(lua_script)(keys=[key], args=[step, time])
        return res

    def __getattr__(self, name):
        """
        the __getattr__() method is actually a fallback method
        that only gets called when an attribute is not found
        """
        return getattr(self._client, name)

    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            print('setattr:', name, value)
            setattr(self._client, name, value)

    def __delattr__(self, name):
        if name.startswith('_'):
            super().__delattr__(name)
        else:
            print('delattr:', name)
            delattr(self._client, name)
