from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class Staff(db.Model,UserMixin):
  __tablename__="Staff"
  id=db.Column(db.Integer(),primary_key=True)
  first_name=db.Column(db.String(25),nullable=False)
  last_name=db.Column(db.String(25),nullable=False)
  email=db.Column(db.String(50),nullable=False)
  password=db.Column(db.String(100),nullable=False)

class Clients(db.Model):
  __tablename__ = "client_records"
  id = db.Column(db.Integer(), primary_key=True)
  full_name = db.Column(db.String(50), nullable=False)
  location = db.Column(db.String(300), nullable=False)
  phone_number_1 = db.Column(db.String(20))
  phone_number_2 = db.Column(db.String(20))
  client_disease = db.relationship("ClientDisease", backref="disease_client", lazy=True)
  client_medicine = db.relationship("ClientMedicine", backref="medicine_client", lazy=True)

class Diseases(db.Model):
  __tablename__ = "diseases"
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  client_disease = db.relationship("ClientDisease", backref="client_disease", lazy=True)

class Medicine(db.Model):
  __tablename__ = "medicine"
  id = db.Column(db.Integer(), primary_key=True)
  name = db.Column(db.String(50), nullable=False)
  client_medicine = db.relationship("ClientMedicine", backref="client_medicine", lazy=True)

class ClientDisease(db.Model):
  __tablename__ = 'client_disease'
  id = db.Column(db.Integer(), primary_key=True)
  client_id = db.Column(db.Integer(), db.ForeignKey("client_records.id"))
  disease_id = db.Column(db.Integer(), db.ForeignKey("diseases.id"))

class ClientMedicine(db.Model):
  __tablename__ = 'client_medicine'
  id = db.Column(db.Integer(), primary_key=True)
  client_id = db.Column(db.Integer(), db.ForeignKey("client_records.id"))
  medicine_id = db.Column(db.Integer(), db.ForeignKey("medicine.id"))
