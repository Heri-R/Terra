class Config:
  SQLALCHEMY_DATABASE_URI = "sqlite:///backup.db"
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SESSION_PERMANENT = False
  SESSION_TYPE = "filesystem"
  SECRET_KEY= "skey"