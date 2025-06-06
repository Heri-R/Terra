import os

class Config:
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://", 1) 
  # SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://DESKTOP-8QPF538/terra_herb?driver=ODBC+Driver+17+for+SQL+Server" 
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SESSION_PERMANENT = False
  SESSION_TYPE = "filesystem"
  SECRET_KEY= "jhbfjhwebfjhewbfbwejhfbwejfh"