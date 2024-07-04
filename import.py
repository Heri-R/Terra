from flask import Flask
import csv
from models import Clients, db, Diseases, Medicine
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def add_clients():
  user_file = open("clients.csv")
  read_files = csv.reader(user_file)

  for name, location, phone1, phone2 in read_files:
    new_client = Clients(
      full_name = name,
      location = location,
      phone_number_1 = phone1,
      phone_number_2 = phone2,
    )
    db.session.add(new_client)
    db.session.commit()

def add_diseases():
  user_file = open("Disease2.csv")
  read_files = csv.reader(user_file)

  for names in read_files:
    for name in names:
      new_disease = Diseases(
        name = name
      )
      db.session.add(new_disease)
      db.session.commit()

def add_medicine():
  user_file = open("Medicine2.csv")
  read_files = csv.reader(user_file)

  for names in read_files:
    for name in names:
      if name:
        new_medicine = Medicine(
          name = name
        )
        db.session.add(new_medicine)
        db.session.commit()

if __name__ == "__main__":
  with app.app_context():
    add_clients()
    # add_diseases()
    # add_medicine()
