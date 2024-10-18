class Config:
  SQLALCHEMY_DATABASE_URI = "mssql+pyodbc://DESKTOP-8QPF538/terra_herb?driver=ODBC+Driver+17+for+SQL+Server"
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SESSION_PERMANENT = False
  SESSION_TYPE = "filesystem"
  SECRET_KEY= "jhbfjhwebfjhewbfbwejhfbwejfh"