from dotenv import load_dotenv
import os

load_dotenv()

class Config:
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://", 1)
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SESSION_PERMANENT = False
  SESSION_TYPE = "filesystem"
  SECRET_KEY = os.environ.get("SECRET_KEY")
  CACHE_TYPE = "SimpleCache"
  # CACHE_REDIS_PORT = 19509
  CACHE_DEFAULT_TIMEOUT = 300
  # CELERY = {
  #   "broker_url": "redis-cli -u redis://default:112NFxZ0FIXEzcnKZGTYqCPWrMnHLNc2@redis-19509.c270.us-east-1-3.ec2.redns.redis-cloud.com:19509",
  #   "result_backend": "redis-cli -u redis://default:112NFxZ0FIXEzcnKZGTYqCPWrMnHLNc2@redis-19509.c270.us-east-1-3.ec2.redns.redis-cloud.com:19509",
  # }
