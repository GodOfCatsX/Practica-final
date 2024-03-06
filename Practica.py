from flask import Flask, request, render_template, redirect, url_for, session
import mysql.connector
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/",methods = ['POST', 'GET'])
def index():
   return render_template("PEInicipublic.html")

@app.route("/pagina_privada")
def private_page():
   if request.method == "GET" and session.get("username"):
      return render_template("PEIniciprivate.html")
   else:
      return render_template("PEInicipublic.html")

@app.route("/login",methods = ['POST', 'GET'])
def login():
      if request.method == 'POST':
         mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="web"
         )
         username = request.form["username"]
         password = request.form["password"]
         cursor = mydb.cursor()
         users = cursor.execute(f"SELECT * FROM datos WHERE nombre = '{username}' AND password_yes = '{password}'")
         users = cursor.fetchall()
         if len(users) > 0:
            session["username"] = username + password
            return render_template("PEIniciprivate.html")
         else:
            return render_template("PEerror.html")
      if request.method == "GET":
         return render_template('PELogin.html')

@app.route("/register",methods=['POST','GET'])
def register_user():
   print("pep")
   if request.method == 'GET':
      return render_template("PERegister.html")
   if request.method == 'POST':
      mydb = mysql.connector.connect(
         host="localhost",
         user="root",
         password="",
         database="web"
      )
      username = request.form["username"]
      password = request.form["password"]
      confirm_password = request.form["confirm_password"]
      if password == confirm_password:
         cursor = mydb.cursor()
         cursor.execute(f"INSERT INTO datos (nombre,password_yes) VALUES ('{username}', '{password}')")
         mydb.commit()
         return render_template("PERegister.html", mensaje = f"Registrado el usuario {username}")
      else:
         return render_template("PERegister.html", mensaje = "Pon bien las dos contraseñas")

@app.route("/formularios")
def formulario_joao():
   return render_template("Formularios.html")

@app.route("/logout")
def logout():
   if session.get('username'):
      session.pop('username', default=None)
      return redirect("/")