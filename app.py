from flask import Flask,flash,request,redirect,url_for,render_template
from models import db, Staff, Clients, Diseases, Medicine, ClientDisease, ClientMedicine, ClientLocation, ClientPayment
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, login_manager
from flask_bcrypt import Bcrypt
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app,db)
login_manager=LoginManager()
login_manager.login_view="/Login"
login_manager.login_message="Please Login or Sign Up to access this page"
login_manager.login_message_category="danger"
login_manager.init_app(app)
bcrypt = Bcrypt()

@login_manager.user_loader
def load_user(user_id):
  try:
    return Staff.query.filter_by(id=user_id).first()
  except:
    flash(f"Failed to login the user", category="danger")

@app.route("/register", methods=["POST","GET"])
def register():
  staff_count = Staff.query.count()
  print(staff_count)
  if request.method=="POST":
    emailaddress=Staff.query.filter_by(email=request.form.get("email3")).first()
    if emailaddress: 
      print("This Email already exists")
      return redirect(url_for("register"))
    elif request.form.get("password4") != request.form.get("password5"):
      print("This password did not match")
      return redirect(url_for("register"))
    elif staff_count == 2:
      flash("Only 2 user accounts are allowed", category="warning")
      return redirect(url_for("register"))
    else:
      new_staff=Staff(
        first_name=request.form.get("firstname1"),
        last_name=request.form.get("lastname2"), 
        email=request.form.get("email3"), 
        password=bcrypt.generate_password_hash(request.form.get("password4")).decode("utf-8"),      
      )
      db.session.add(new_staff)
      db.session.commit()
      print("New staff added")
      return redirect(url_for("Login"))

  return render_template("register.html")

@app.route("/Login", methods=["POST","GET"])
def Login():
  if request.method=="POST":
    email=request.form.get("email3")
    password=request.form.get("password4")
    user=Staff.query.filter_by(email=email).first()
    if user is None:
      flash("This email address doesn't exist",category="danger")
      return redirect(url_for("Login"))
    else:
      if bcrypt.check_password_hash(user.password, password):
        login_user(user)
        flash("Login successful", category="success")
        next=request.args.get("next")
        return redirect(next or url_for("home"))
      else:
        flash("This password is incorrect",category="danger")
        return redirect(url_for("Login"))
  
  return render_template("Login.html")

@app.route("/Logout")
def Logout():
  logout_user()
  flash("Logout successful", category="success")
  return redirect(url_for("Login"))

@app.route("/")
@app.route("/home")
def home():
  clients = Clients.query.all()
  medicines = Medicine.query.all()
  client_medicines = ClientMedicine.query.filter_by(is_paid=False).all()

  return render_template("home.html",clients=clients, medicines=medicines, client_medicines=client_medicines)

@app.route("/Clients")
def Client():
  """
  querying/getting/retreiving data from database
  client records table
  10 records

  get data

  Must
  1. Class Name
  2. Query - get the data
  optional
  3. filter
  4. Number of records - (first | all)
  """

  """
  Clients.query.all() -> a bunch objects(1115)
  object1 -> clients, object2 -> clients
  [object1,object2......object1115] -> clients

  for loop -> access the objects
  """

  clients = Clients.query.all()

  return render_template("client.html",clients=clients)


@app.route("/Diseases")
def Disease():
  diseases = Diseases.query.all()
  return render_template("disease.html",diseases=diseases)

@app.route("/edit-disease/<int:disease_id>", methods=["POST", "GET"])
def edit_disease(disease_id):
  disease = Diseases.query.get(disease_id)
  if not disease:
    flash("disease not found", category="danger")
    return redirect(url_for("Disease"))
  if request.method == "POST":
    disease.name = request.form.get("dname")
    db.session.commit()
    flash("Disease record updated successfully", category="success")
    return redirect(url_for('Disease'))
  else:
    return render_template("new_disease.html", disease=disease)

@app.route("/remove-disease/<int:disease_id>")
def remove_disease(disease_id):
  disease = Diseases.query.get(disease_id)
  if not disease:
    flash("Disease not found", category="danger")
  else:
    db.session.delete(disease)
    db.session.commit()
    flash("Disease removed successfully", category="success")
  return redirect(url_for("Disease"))

@app.route("/Medicine")
def Medicines():
  medicines = Medicine.query.all()
  return render_template("medicine.html",medicines=medicines)

@app.route("/edit-medicine/<int:medicine_id>", methods=["POST", "GET"])
def edit_medicine(medicine_id):
  medicine = Medicine.query.get(medicine_id)
  if not medicine:
    flash("medicine not found", category="danger")
    return redirect(url_for("Medicine"))
  if request.method == "POST":
    medicine.name = request.form.get("Mname")
    db.session.commit()
    flash("Medicine record updated successfully", category="success")
    return redirect(url_for('Medicines'))
  else:
    return render_template("new_medicine.html", medicine=medicine)

@app.route("/prescribe-patient/<int:patient_id>", methods=["POST"])
def prescribe_patient(patient_id):
  patient = Clients.query.get(patient_id)
  medicine = Medicine.query.get(request.form.get("medication"))
  """
  check the quantity of the medicine to be prescribed
  if the quantity is greater than 0 or if the quantity is less than 1
  if it is -> presribe
  update the quantity -> deduct
  if it's not flash a message
  """
  if medicine.quantity > 0:
    client_medicine = ClientMedicine(
      client_id = patient.id,
      medicine_id = medicine.id
    )
    db.session.add(client_medicine)
    medicine.quantity = medicine.quantity - 1
    db.session.commit()
    flash("Medicine prescribed successfully", category="success")
  else:
    flash("Out of Stock kindly restock", category="warning")
    return redirect(url_for('medicine_stock',medicine_id=medicine.id))

  return redirect(url_for('home'))

@app.route("/medicine-payment/<int:client_id>")
def medicine_payment(client_id):
  # The client
  # The prescription's associated with the client - More than 1
  # The status of the prescription
  #   -> if is_paid is False -> mark that prescription as paid
  
  client = Clients.query.get(client_id)
  if not client:
    flash("Client not found", category="danger")
    return redirect(url_for("home"))
  client_pescription = ClientMedicine.query.filter_by(client_id = client.id, is_paid = False).all()
  total = sum([medicine.price for medicine in Medicine.query.all() for prescription in client_pescription if medicine.id == prescription.medicine_id])
  new_payment = ClientPayment(
    amount = total,
    is_paid = True,
    date_paid = datetime.now()
  )
  db.session.add(new_payment)
  db.session.commit()
  for prescption in client_pescription:
    prescption.client_payment_id = new_payment.id
    prescption.is_paid = True 
  db.session.commit()
  flash("Payment successfull", category="success")
  return redirect(url_for("clients_detail", clients_id=client.id))

@app.route("/medicine-stock/<int:medicine_id>", methods=["POST","GET"])    
def medicine_stock(medicine_id):
  medicine = Medicine.query.get(medicine_id)
  if request.method == "POST":
    stock_amount = request.form.get("stock")
    medicine.quantity = stock_amount
    db.session.commit()
    flash("Stock added succesfully", category='success')

  return render_template("stock.html",medicine=medicine)

@app.route("/remove-medicine/<int:medicine_id>")
def remove_medicine(medicine_id):
  medicine = Medicine.query.get(medicine_id)
  if not medicine:
    flash("Medicine not found", category="danger")
  else:
    db.session.delete(medicine)
    db.session.commit()
    flash("Medicine removed successfully", category="success")
  return redirect(url_for("home"))

@app.route("/Client_details/<int:clients_id>")
def clients_detail(clients_id):
  clients_details = Clients.query.get(clients_id)
  all_diseases = Diseases.query.all()
  all_medicines = Medicine.query.all()
  locations = ClientLocation.query.all()
  client_diseases = ClientDisease.query.filter_by(client_id=clients_details.id).all()
  client_medicines= ClientMedicine.query.filter_by(client_id=clients_details.id).all()
  client_payments = ClientPayment.query.all()

  if not clients_details:
    return "Invalid client ID. No matching client found"
  return render_template('client_details.html', clients_details=clients_details, all_diseases=all_diseases, client_diseases=client_diseases,all_medicines=all_medicines,client_medicines=client_medicines, locations=locations, client_payments=client_payments)

@app.route("/edit-client/<int:client_id>", methods=["POST", "GET"])
def edit_client(client_id):
  client = Clients.query.get(client_id)
  if not client:
    flash("Client not found", category="danger")
    return redirect(url_for("Client"))
  if request.method == "POST":
    client.full_name = request.form.get("fname")
    client.location = request.form.get("loc1")
    client.phone_number_1 = request.form.get("phone1")
    client.phone_number_2 = request.form.get("phone2")
    client.age = request.form.get("age")
    client.gender = request.form.get("Gender")
    db.session.commit()
    flash("Client record updated successfully", category="success")
    return redirect(url_for('Client'))
  else:
    return render_template("new_patient.html", client=client)

@app.route("/update-location/<int:patient_id>", methods=["POST"])
def update_location(patient_id):
  """
  ID the client - From DB
  handle the form submission
    - Route must handle POST request
    - 1st input - location input field (name of 'location')
      - The location ID - INT
    - 2nd input - specific location input field (name of 'specific_location')
      - Name of the specific location - String

  Save our db - with the changes
  redirect to the client details page
  """
  client = Clients.query.get(patient_id)
  location_name = request.form.get("location")
  specific_location = request.form.get("specific_location")
  client.location = location_name
  client.specific_location = specific_location

  db.session.commit()
  flash("Loaction saved succesfully", category="success")
  return redirect(url_for('clients_detail',clients_id=client.id))

@app.route("/diagnose-patient/<int:patient_id>", methods=["POST"])
def diagnose_patient(patient_id):
  patient = Clients.query.get(patient_id)
  disease = Diseases.query.get(request.form.get("disease"))
  client_disease = ClientDisease(
    client_id = patient.id,
    disease_id = disease.id
  )
  db.session.add(client_disease)
  db.session.commit()
  flash("Patient diaginosed successfully", category="success")
  return redirect(url_for('clients_detail', clients_id=patient.id))

@app.route("/Client_delete/<int:clients_id>")
def clients_delete(clients_id):
  client_delete = Clients.query.get(clients_id)
  if not client_delete:
    flash('Cannot delete a record that does not exist',category="danger")

  db.session.delete(client_delete)
  db.session.commit()

  flash('Record deleted succesfuly',category="success")
  return redirect(url_for('Client'))

  
@app.route("/New_patient", methods=["GET", "POST"])
def New_patient():
  if request.method=="POST":
    full_name = request.form.get("fname")
    Phonenumber1 = request.form.get("phone1")
    Phonenumber2 = request.form.get("phone2")
    age = request.form.get("age")
    gender = request.form.get("Gender")

    Add_patient = Clients(
      full_name = full_name,
      phone_number_1 = Phonenumber1,
      phone_number_2 = Phonenumber2,
      age = age,
      gender = gender,
    )
    db.session.add(Add_patient)
    db.session.commit()
    flash("Details added", category='success')
    
    return redirect(url_for('Client'))
  return render_template('new_patient.html')

@app.route("/New_disease", methods=["GET", "POST"])
def New_disease():
  if request.method == "POST":
    Disease_name=request.form.get("dname")
    
    Add_Disease = Diseases(
      name = Disease_name,
      
    )
    db.session.add(Add_Disease)
    db.session.commit()
    flash("Disease added", category='success')
    return redirect(url_for('Disease'))
  return render_template('new_disease.html')

@app.route("/New_medicine", methods=["GET", "POST"])
def New_medicine():

  if request.method == "POST":
    Medicine_name=request.form.get("Mname")
    Medicine_price=request.form.get("Mprice")

    Add_Medicine = Medicine(
      name = Medicine_name,
      price = Medicine_price,
    )
    db.session.add(Add_Medicine)
    db.session.commit()
    flash("Medicine added", category='success')
    return redirect(url_for('home'))
  return render_template('new_medicine.html')

if __name__ == "__main__":
  app.run(debug=True)
