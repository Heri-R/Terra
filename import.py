from flask import Flask
import csv
from models import Clients, db, Diseases, Medicine, ClientLocation
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def add_clients():
  user_file = open("clients.csv")
  read_files = csv.reader(user_file)

  for name, age, gender, phone1, phone2 in read_files:
    new_client = Clients(
      full_name = name,
      phone_number_1 = phone1,
      phone_number_2 = phone2,
      age = age,
      gender = gender,
    )
    db.session.add(new_client)
    db.session.commit()

def add_location():
  user_file = open("Locations_data.csv")
  read_files = csv.reader(user_file)

  for region, district in read_files:
    new_location = ClientLocation(
      region = region,
      district = district,
    )
    db.session.add(new_location)
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
  user_file = open("Price list.csv")
  read_files = csv.reader(user_file)

  for name, price in read_files:
    new_medicine = Medicine(
      name = name,
      price = price,
    )
    db.session.add(new_medicine)
    db.session.commit()

if __name__ == "__main__":
  with app.app_context():
    add_clients()
    add_diseases()
    add_medicine()
    add_location()
