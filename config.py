from dotenv import load_dotenv
import os
from urllib.parse import urlparse
import redis

load_dotenv(override=True)

class Config:
  SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL").replace("postgres://", "postgresql://", 1)
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SESSION_PERMANENT = False
  SESSION_TYPE = "filesystem"
  SECRET_KEY = os.environ.get("SECRET_KEY")
  CACHE_TYPE = "RedisCache"
  CACHE_REDIS_URL = os.environ.get("HEROKU_REDIS_SILVER_URL")
  r = redis.Redis(host=CACHE_REDIS_URL.hostname, port=CACHE_REDIS_URL.port, password=CACHE_REDIS_URL.password, ssl=(CACHE_REDIS_URL.scheme == "rediss"), ssl_cert_reqs=None)

