import redis
import json
from .config import Config

class RedisClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisClient, cls).__new__(cls)
            cls._instance.client = redis.from_url(Config.REDIS_URL)
        return cls._instance

    def get_channel_users(self, channel_name):
        users_key = f"channel:{channel_name}:users"
        users_data = self.client.hgetall(users_key)
        return [json.loads(user_data) for user_data in users_data.values()]

    def add_channel_user(self, channel_name, user_data):
        users_key = f"channel:{channel_name}:users"
        self.client.hset(users_key, user_data['uid'], json.dumps(user_data))
        # Set expiration for user data (30 seconds)
        self.client.expire(users_key, 30)

    def remove_channel_user(self, channel_name, uid):
        users_key = f"channel:{channel_name}:users"
        self.client.hdel(users_key, uid)

        # If no users left, remove channel
        if self.client.hlen(users_key) == 0:
            self.client.delete(users_key)

    def update_user_heartbeat(self, channel_name, uid):
        users_key = f"channel:{channel_name}:users"
        user_data = self.client.hget(users_key, uid)
        if user_data:
            user = json.loads(user_data)
            user['last_active'] = datetime.now().isoformat()
            self.client.hset(users_key, uid, json.dumps(user))
            self.client.expire(users_key, 30)
