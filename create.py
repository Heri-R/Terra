from flask import Flask
from models import db, StaffRoles
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
  new_role = StaffRoles(
    name = "Admin"
  )
  db.session.add(new_role)
  db.session.commit()
  print("Admin role added")
  new_role = StaffRoles(
    name = "Clerk"
  )
  db.session.add(new_role)
  db.session.commit()
  print("clerk role added")
  new_role = StaffRoles(
    name = "Stock Controller"
  )
  db.session.add(new_role)
  db.session.commit()
  print("Stock Controller role added")
  new_role = StaffRoles(
    name = "Accountant"
  )
  db.session.add(new_role)
  db.session.commit()
  print("Accountant role added")

if __name__ == "__main__":
  with app.app_context():
    drop_tables()
    create_tables()
    add_roles()
