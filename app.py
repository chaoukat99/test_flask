from flask import Flask, render_template, redirect, jsonify,request
from flask_mysqldb import MySQL
app = Flask(__name__)
# mysql configuration
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="projet"
mysql=MySQL(app)
@app.route('/')
def index():
    return render_template('home.html')
    cursor= mysql.connection.cursor()
    query= cursor.execute("select * from admins")
    if query:
        result=cursor.fetchall()
    return render_template("home.html")
@app.route("/admin-dash")
def dashadmin():
     return render_template("dashadmin.html")
@app.route("/projectmanager-dash")
def dashpm():
     return render_template("dashpm.html")
@app.route("/engineer-dash")
def dashengineer():
     return render_template("dashengineer.html")
@app.route('/login-admin')
def login_admin_view():
    return render_template("logadmin.html")
@app.route('/login-engineer')
def login_engineer_view():
    return render_template("logen.html")
@app.route('/login-projectmanager')
def login_pm_view():
    return render_template("logpm.html")
@app.route("/error")
def error():
    return render_template("error.html")
@app.route('/check-admin-login', methods=["POST"])
def check_log_admin():
    if request.method== "POST":
        username= request.form["username"]
        password= request.form["password"]
        cursor= mysql.connection.cursor()
        query= cursor.execute("SELECT * FROM admins WHERE email=%s AND pass=%s", (username,password))
        if query:
            result= cursor.fetchall()
            if result:
                return jsonify(result)
        else:
                return """<body><script src="https://cdn.jsdelivr.net/npm/sweetalert2@11">
                </script>
                <script>setTimeout(()=>{
           Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'You are Not Allowed to view this page',
            footer: '<a href="/login-admin">Back to login</a>',
            showConfirmButton:false
          })
        },1000)
        </script><h1 style='display:none'>you are not allowed</h1></body>
                """
@app.route('/check-engineer-login', methods=["POST"])
def check_log_engineer():
    if request.method== "POST":
        username= request.form["username"]
        password= request.form["password"]
        cursor= mysql.connection.cursor()
        query= cursor.execute("SELECT * FROM ingenieur WHERE email=%s AND password=%s", (username, password))
        if query:
            result= cursor.fetchall()
            if result:
                return jsonify(result)
        else:
                return """<body><script src="https://cdn.jsdelivr.net/npm/sweetalert2@11">
                </script>
                <script>setTimeout(()=>{
           Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'You are Not Allowed to view this page',
            footer: '<a href="/login-engineer">Back to login</a>',
            showConfirmButton:false
          })
        },1000)
        </script><h1 style='display:none'>you are not allowed</h1></body>
                """
@app.route('/check-projectmanager-login', methods=["POST"])
def check_log_prpjectmanager():
    if request.method== "POST":
        username= request.form["username"]
        password= request.form["password"]
        cursor= mysql.connection.cursor()
        query= cursor.execute("SELECT * FROM chef_projet WHERE username=%s AND password=%s", (username, password))
        if query:
            result= cursor.fetchall()
            if result:
                return jsonify(result)
        else:
                return """<body><script src="https://cdn.jsdelivr.net/npm/sweetalert2@11">
                </script>
                <script>setTimeout(()=>{
           Swal.fire({
            icon: 'error',
            title: 'Oops...',
            text: 'You are Not Allowed to view this page',
            footer: '<a href="/login-projectmanager">Back to login</a>',
            showConfirmButton:false
          })
        },1000)
        </script><h1 style='display:none'>you are not allowed</h1></body>
                """





if __name__ == "__main__":
    app.run(debug=True)

