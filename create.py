from flask import Flask
from Models.base_model import db
from Models.users import *
from Models.diagnosis import *
from Models.prescription import *
from Models.diseases import *
from Models.medicine import *
from Models.payment import *
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def create_tables():
  db.create_all()
  print("Tables created successully")

def drop_tables():
  db.drop_all()
  print("Tables dropped successully")

def add_roles():
  roles = ["Admin", "Clerk", "Stock Controller", "Accountant", "Lab Tech"]
  for role in roles:
    new_role = Role(
      name = role
    )
    db.session.add(new_role)
    db.session.commit()
    print(f"{role} role added")

def test_user():
  new_user = Patients(
    first_name = "Test",
    last_name = "Test",
    age = 20,
    phone_number_1 = "0786543245",
    phone_number_2 = "0786543241",
  )
  db.session.add(new_user)
  db.session.commit()
  print("Test user added")

if __name__ == "__main__":
  with app.app_context():
    drop_tables()
    create_tables()
    add_roles()
    # test_user()
