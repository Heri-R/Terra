from dotenv import load_dotenv
import os
from urllib.parse import urlparse
import redis

load_dotenv(override=True)

class Config:
  SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SESSION_PERMANENT = False
  SESSION_TYPE = "filesystem"
  SECRET_KEY = os.environ.get("SECRET_KEY")
  CACHE_TYPE = "RedisCache"
  CACHE_REDIS_URL = os.environ.get("REDIS_URL")
 

