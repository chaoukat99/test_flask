from flask import Flask, render_template,session, redirect, jsonify,request
from flask_mysqldb import MySQL
import secrets
app = Flask(__name__)


# sET SECRET 
secret_key=secrets.token_hex(16)
app.secret_key=secret_key

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
@app.route("/create-ing")
def createing():
     return render_template("create-ing.html")
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

        # Statistics 
        cursor_admin=mysql.connection.cursor()
        query_cursor2=cursor_admin.execute("SELECT count(*) FROM admins")
        if query_cursor2:
             num_admin = cursor_admin.fetchall()

        #  Project Manager
        cursor_chef=mysql.connection.cursor()
        query_cursor3=cursor_chef.execute("SELECT count(*) FROM chef_projet")
        if query_cursor3:
             chef_count = cursor_chef.fetchall()
        
        #Enginner 
        cursor_eng=mysql.connection.cursor()
        query_cursor4=cursor_eng.execute("SELECT count(*) FROM ingenieur")
        if query_cursor4:
             num_eng = cursor_eng.fetchall()
        # Projects

        cursor_prj=mysql.connection.cursor()
        query_cursor5=cursor_prj.execute("SELECT DISTINCT COUNT(*) FROM projet")
        if query_cursor5:
             num_prj=cursor_prj.fetchall()
        if query:
            result= cursor.fetchall()
            if result:
                # return jsonify(result)
                # if admin log in successfully we need to create  session
                session["admin_logged"]=True
                session["admin_data"]=result   
                session["count_admins"]= num_admin            
                session["count_chefs"]= chef_count            
                session["count_eng"]= num_eng         
                session["count_projet"]= num_prj  

                return redirect("/admin-dash",302)
               
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
        
@app.route("/deconn-admin")
def deconn():
     session["admin_logged"]=False
     return redirect("/",302)  


# deconnexion pm


@app.route("/deconn-pm")
def deconn2():
     session["pm_logged"]=False
     return redirect("/")

# deconn engineer

@app.route("/deconn-eng")
def deconn3():
     session["eng_logged"]=False
     return redirect("/")
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
                session["eng_logged"]=True
                session["eng_data"]=result
                return redirect("/engineer-dash",302)
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
                session["pm_logged"]=True
                session["pm_data"]=result
                cursor_projects_of_pm=mysql.connection.cursor()
                query_projects=cursor_projects_of_pm.execute("SELECT count(id_projet) FROM projet WHERE id_chef_trg=%s",(str(result[0][0])))
                if query_projects:
                    project_pm=cursor_projects_of_pm.fetchall() 
                    if project_pm:
                         session["project_pm"]=project_pm
                    
                return redirect("/projectmanager-dash",302)
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

