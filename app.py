from flask import Flask,flash,request,redirect,url_for,render_template
from models import db,Staff,Clients,Diseases,Medicine
from flask_migrate import Migrate
from config import Config
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, login_manager
from flask_bcrypt import Bcrypt

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
  return render_template("home.html")

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

@app.route("/remove-medicine/<int:medicine_id>")
def remove_medicine(medicine_id):
  medicine = Medicine.query.get(medicine_id)
  if not medicine:
    flash("Medicine not found", category="danger")
  else:
    db.session.delete(medicine)
    db.session.commit()
    flash("Medicine removed successfully", category="success")
  return redirect(url_for("Medicines"))

@app.route("/Client_details/<int:clients_id>")
def clients_detail(clients_id):
  clients_details = Clients.query.get(clients_id)
  if not clients_details:
    return "Invalid client ID. No matching client found"
  return render_template('client_details.html', clients_details=clients_details)

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
    db.session.commit()
    flash("Client record updated successfully", category="success")
    return redirect(url_for('Client'))
  else:
    return render_template("new_patient.html", client=client)

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
    location = request.form.get("loc1")
    Phonenumber1 = request.form.get("phone1")
    Phonenumber2 = request.form.get("phone2")

    Add_patient = Clients(
      full_name = full_name,
      location = location,
      phone_number_1 = Phonenumber1,
      phone_number_2 = Phonenumber2,
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

    Add_Medicine = Medicine(
      name = Medicine_name,
    )
    db.session.add(Add_Medicine)
    db.session.commit()
    flash("Medicine added", category='success')
    return redirect(url_for('Medicines'))
  return render_template('new_medicine.html')




if __name__ == "__main__":
  app.run(debug=True)
