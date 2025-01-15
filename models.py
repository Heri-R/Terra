from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class StaffRoles(db.Model):
  __tablename__="staff_roles"
  id=db.Column(db.Integer(),primary_key=True)
  name = db.Column(db.String(), nullable=False)
  staff = db.relationship("Staff", backref="staff_role", lazy=True)

class Staff(db.Model,UserMixin):
  __tablename__="Staff"
  id=db.Column(db.Integer(),primary_key=True)
  first_name=db.Column(db.String(25),nullable=False)
  last_name=db.Column(db.String(25),nullable=False)
  email=db.Column(db.String(50),nullable=False)
  role = db.Column(db.Integer(), db.ForeignKey('staff_roles.id'))
  password=db.Column(db.String(100),nullable=False)

class Clients(db.Model):
  __tablename__ = "client_records"
  id = db.Column(db.Integer(), primary_key=True)
  full_name = db.Column(db.String(50), nullable=False)
  age = db.Column(db.Integer())
  gender = db.Column(db.String(6))
  phone_number_1 = db.Column(db.String(20))
  phone_number_2 = db.Column(db.String(20))
  client_disease = db.relationship("ClientDisease", backref="disease_client", lazy=True)
  client_medicine = db.relationship("ClientMedicine", backref="medicine_client", lazy=True)
  location = db.Column(db.Integer(), db.ForeignKey("client_location.id"))
  specific_location = db.Column(db.String(30))
  
class ClientLocation(db.Model):
  id = db.Column(db.Integer(), primary_key=True)
  __tablename__ = "client_location"
  region = db.Column(db.String(20))
  district = db.Column(db.String(30))
  client = db.relationship("Clients", backref="client_location", lazy=True)

class Diseases(db.Model):
  __tablename__ = "diseases"
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  client_disease = db.relationship("ClientDisease", backref="client_disease", lazy=True)

class Medicine(db.Model):
  __tablename__ = "medicine"
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.Text(), nullable=False)
  price = db.Column(db.Integer(), default=0)
  quantity = db.Column(db.Integer(), default=0)
  prescription = db.relationship("Prescriptions", backref="prescription_medicine", lazy=True)

class ClientDisease(db.Model):
  __tablename__ = 'client_disease'
  id = db.Column(db.Integer(), primary_key=True)
  client_id = db.Column(db.Integer(), db.ForeignKey("client_records.id"))
  disease_id = db.Column(db.Integer(), db.ForeignKey("diseases.id"))

class ClientMedicine(db.Model):
  __tablename__ = 'client_medicine'
  id = db.Column(db.Integer(), primary_key=True)
  client_id = db.Column(db.Integer(), db.ForeignKey("client_records.id"))
  client_payment_id = db.Column(db.Integer(), db.ForeignKey("client_payment.id"))
  is_paid = db.Column(db.Boolean(), default=False)
  prescription = db.relationship("Prescriptions", backref="prescriptions", lazy=True)

class Prescriptions(db.Model):
  __tablename__ = 'prescriptions'
  id = db.Column(db.Integer(), primary_key=True)
  medicine_id = db.Column(db.Integer(), db.ForeignKey("medicine.id"))
  client_medicine_id = db.Column(db.Integer(), db.ForeignKey("client_medicine.id"))

class ClientPayment(db.Model):
  __tablename__ = 'client_payment'
  id = db.Column(db.Integer(), primary_key=True)
  amount = db.Column(db.Integer(), default=0)
  is_paid = db.Column(db.Boolean(), default=False)
  date_paid = db.Column(db.DateTime())
  client_medicine_id = db.relationship("ClientMedicine", backref="Medicine_Payment", lazy=True)
