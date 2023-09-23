from flask import Flask, render_template,session, redirect, jsonify,url_for,request,get_flashed_messages , flash
import json
from flask_mysqldb import MySQL
import secrets
app = Flask(__name__)

#   Dictionnary fun 
def dictt(arr):
     if(len(arr)>1):
          array_of_objects=map(lambda x:{"id":x[0],"name_p":x[1],"ing_name":x[2],"status":x[3],"date_debut":x[4],"date_fin":x[5]},arr)
          return join_engineers(list(array_of_objects))
     elif len(arr) == 1: 
          return [{"id":arr[0][0],"name_p":arr[0][1],"ing_name":arr[0][2],"status":arr[0][3],"date_debut":arr[0][4],"date_fin":arr[0][5]}]
     else : 
          return [] 
               



def join_engineers(eng_list):
    # Create a dictionary to store engineers by project
    project_eng = {}

    # Iterate through the list of dictionaries and group engineers by project
    for entry in eng_list:
        engineer = entry['ing_name']
        project = entry['name_p']
        if project in project_eng:
            project_eng[project]['ing_name'].append(engineer)
        else:
            project_eng[project] = {
                 'id': entry.get('id',None),
                'ing_name': [engineer],
                'status': entry.get('status', None),
                'date_debut': entry.get('date_debut', None),
                'date_fin': entry.get('date_fin', None)
            }

    # Create a list of dictionaries to store the result
    result = []

    # Iterate through the dictionary and format the output
    for project, project_data in project_eng.items():
        engineers_str = ', '.join(project_data['ing_name'])
        result.append({
             "id":project_data["id"],
            'name_p': project,
            'ing_name': engineers_str,
            'status': project_data['status'],
            'date_debut': project_data['date_debut'],
            'date_fin': project_data['date_fin']
        })

    return result



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
@app.route("/admin-statistics")
def statisticsadmin():
      cursor_chart= mysql.connection.cursor()
      query_chart=cursor_chart.execute("""SELECT chef_projet.username AS chef_name , COUNT(projet.id_projet) as nb  FROM projet 
          join chef_projet on chef_projet.id_chef_prj=projet.id_chef_trg GROUP BY chef_projet.username""")
      if query_chart:
             chart_1= cursor_chart.fetchall()
             chart_1_array=list(chart_1)
             final_data=[list(t) for t in chart_1_array]
             json_data=json.dumps(final_data)
             session["data_session"]=final_data
          #    chart_1_array.insert(0,["project managers","project's numbers"])
          #    return render_template("statistics-admin.html")
             
             return render_template("statistics-admin.html")
            
             return "shshs"
      
@app.route("/admin-profile")
def profileadmin():
     return render_template("profile-admin.html")
@app.route("/engineer-profile")
def profileengineer():
     return render_template("profile-engineer.html")
@app.route("/pm-profile")
def profilepm():
     return render_template("profile-pm.html")
@app.route("/pm-statistics")
def statisticspm():
     return render_template("statistics-pm.html")
@app.route("/engineer-statistics")
def statisticsengineer():
     return render_template("statistics-en.html")
@app.route("/admin-dash")
def dashadmin():
     return render_template("dashadmin.html")
@app.route("/create-ing")
def createing():
     return render_template("create-ing.html")
@app.route("/create-pm-admin")
def createpm():
     return render_template("create-pm-admin.html")
@app.route("/projectmanager-dash")
def dashpm():
     # Get projects
     #  flash()
     data_received=get_flashed_messages(category_filter='data') 
     data=session.get("data",[])
     data_received = request.args.get('msg')

    
     return render_template("dashpm.html",projects=data,msg=data_received)
    



# test include

# Add engineer

@app.route("/add-ing",methods=["POST"])
def add_ing():
     if request.method == "POST":
        full_name = request.form["fullname"]
        email = request.form["email"]
        password = request.form["password"]
        dep = request.form["dep"]
        cursor_insert = mysql.connection.cursor()
        query = cursor_insert.execute("INSERT INTO ingenieur(nom_complet,email,departement,password) VALUES (%s,%s,%s,%s )",(full_name, email, dep, password))
        if query:
          mysql.connection.commit()
          cursor_insert.close()
          return redirect(url_for("dashpm",msg="Engineer Added Successfully"))
        else:
         cursor_insert.close()
         return jsonify("unsuccess")


@app.route("/add-pm",methods=["POST"])
def add_pm():
     if request.method == "POST":
        full_name = request.form["fullname"]
        email = request.form["email"]
        phone = request.form["phone number"]
        password = request.form["password"]
        dep = request.form["dep"]
        cursor_insert1 = mysql.connection.cursor()
        query = cursor_insert1.execute("INSERT INTO chef_projet(username,email,phone,departement,password) VALUES (%s,%s,%s,%s,%s )",(full_name, email, phone, dep, password))
        if query:
          mysql.connection.commit()
          cursor_insert1.close()
          return redirect(url_for("dashadmin",msg="Project manager Added Successfully"))
        else:
         cursor_insert1.close()
         return jsonify("unsuccess")



@app.route("/create-project")
def create_p():
     return render_template("create_project.html")


@app.route("/store-project",methods=["POST"])
def store_project():
     p_name=request.form["p_name"]
     date_d=request.form["date_d"]
     date_f=request.form["date_f"]
     id_pm=session["pm_data"][0][0]
     cursor_insert=mysql.connection.cursor()
     query=cursor_insert.execute("INSERT INTO projet(nom_projet,date_debut,date_fin,id_chef_trg) VALUES(%s,%s,%s,%s)",(p_name,date_d,date_f,id_pm))
     if query:
          mysql.connection.commit()
          cursor_insert.close()
          return redirect(url_for("dashpm",msg="Project Created Successfully")) 
     else:
        cursor_insert.close()
        return jsonify("unsuccess")


@app.route("/delete_project")
def project():
      cursor1= mysql.connection.cursor()
      query1=cursor1.execute("SELECT projet.id_projet, projet.nom_projet FROM projet WHERE id_chef_trg=%s",str(session["pm_data"][0][0]))
      if query1:
         project=cursor1.fetchall()
         return render_template("delete_project.html",project=project)
@app.route("/trigger_delete", methods=["POST", "DELETE"])
def delete():
     cursor1= mysql.connection.cursor()
     query1=cursor1.execute("SELECT projet.id_projet, projet.nom_projet FROM projet WHERE id_chef_trg=%s",str(session["pm_data"][0][0]))
     if query1:
         project=cursor1.fetchall()
         cursor_delete=mysql.connection.cursor()
         
     id_p= request.form["p_name"]
     query2=cursor_delete.execute("DELETE FROM projet WHERE id_projet=%d",(int(id_p)))
     if query2 :
           mysql.connection.commit()
           cursor_delete.close()
           return render_template("delete_project.html", project=project)
@app.route("/show_project")
def show_project():
     cursor_task=mysql.connection.cursor()
     query_cursor6=cursor_task.execute("SELECT * FROM tache")  
     if query_cursor6:
             task= cursor_task.fetchall()
             session["task"]=task
     return render_template("show_project.html")     
@app.route("/report")
def report():
     return render_template("report.html")
@app.route("/test_in")
def t_in():
     return render_template("Temp_eng.html")
@app.route("/show_pm")
def show_pm():
     return render_template("show_pm.html")
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
@app.route("/add_task",methods=["POST"])
def addtask():
     
    if request.method== "POST":
         project_name= request.form["p_name"]
         engineer= request.form["engineer"]
         dated= request.form["date_d"]
         datef= request.form["date_f"]
         description= request.form["des"]
         cursor3= mysql.connection.cursor()
         query3= cursor3.execute("INSERT INTO tache(id_projet,id_ing,date_debut,date_fin,libelle) VALUES (%s,%s,%s,%s,%s)",(project_name, engineer, dated, datef ,description))
         if query3:
                    mysql.connection.commit()
                    cursor3.close()
                    return redirect(url_for("dashpm",msg=f"task assigned to engineer with id {engineer}"))
@app.route("/tasks")
def tasks():
    # projet
    cursor1= mysql.connection.cursor()
    query1=cursor1.execute("SELECT projet.id_projet, projet.nom_projet FROM projet WHERE id_chef_trg=%s",str(session["pm_data"][0][0]))
    if query1:
         project=cursor1.fetchall()
    # engineer
    cursor2= mysql.connection.cursor()
    query2=cursor2.execute("SELECT ingenieur.id_ing, ingenieur.nom_complet FROM ingenieur")
    if query2:
         ingenieur1=cursor2.fetchall()
    return render_template("tasks.html",projects=project,ing=ingenieur1)
@app.route("/show_engineers_admin")
def show_engineers_admin():
    return render_template("show_engineers_admin.html")
@app.route("/show_engineers_pm")
def show_engineers_pm():
    return render_template("show_engineers_pm.html")
@app.route("/create-project", methods=["POST"])
def createproject():
     if request.method== "POST":
        project_name= request.form["p_name"]
        dated= request.form["date_d"]
        datef= request.form["date_f"]
        cursor= mysql.connection.cursor()
        query= cursor.execute("INSERT INTO projet(nom_projet,date_debut,date_fin,id_chef_trg) VALUES (%s,%s,%s,%s)",(project_name, dated, datef,session["pm_data"][0][0]))
        if query:
             mysql.connection.commit()
             cursor.close()
     return render_template("create_project.html")

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
        # engineers
        cursor_engineer=mysql.connection.cursor()
        query_cursor6=cursor_engineer.execute("SELECT * FROM ingenieur")  
        if query_cursor6:
             all_engineers= cursor_engineer.fetchall()
             session["all_engineers"]=all_engineers
        # all project managers
        cursor_pm=mysql.connection.cursor()
        query_cursor7=cursor_pm.execute("SELECT * FROM chef_projet")
        if query_cursor7:
             all_pmanagers= cursor_pm.fetchall()
             session["all_pmanagers"]=all_pmanagers
        # all projects
        cursor_projects=mysql.connection.cursor()
        query_cursor9=cursor_pm.execute("SELECT * FROM projet")
        if query_cursor9:
             all_projects= cursor_pm.fetchall()
             session["all_projects"]=all_projects
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
     session.clear()
     return redirect("/",302)  






# deconnexion pm


@app.route("/deconn-pm")
def deconn2():
     session.clear()
     return redirect("/")

# deconn engineer

@app.route("/deconn-eng")
def deconn3():
     session.clear()
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
        


@app.route("/delete")
def del_projet():
     param_url=request.args.get("id_prj")  

     cursor_delete=mysql.connection.cursor()
     query=cursor_delete.execute("DELETE FROM projet WHERE id_projet=%s",(param_url))
     if query :
           mysql.connection.commit()
           cursor_delete.close()
          
           project_cursor=mysql.connection.cursor()
           all_projects_query=project_cursor.execute("""SELECT projet.id_projet , projet.nom_projet ,ingenieur.nom_complet,status , projet.date_debut ,projet.date_fin FROM projet 
JOIN tache on tache.id_projet = projet.id_projet JOIN ingenieur on ingenieur.id_ing = tache.id_ing WHERE projet.id_chef_trg=%s""",(str(session["pm_data"][0][0])))
           if all_projects_query:
                 r_project=project_cursor.fetchall()
                 array_of_p=dictt(r_project)
                 session["data"]=array_of_p 
                 return redirect(url_for("dashpm"))   

       
@app.route('/check-projectmanager-login', methods=["POST"])
def check_log_prpjectmanager():
    if request.method== "POST":
        username= request.form["username"]
        password= request.form["password"]
        cursor= mysql.connection.cursor()
        query= cursor.execute("SELECT * FROM chef_projet WHERE username=%s AND password=%s", (username, password))
        # engineers
        cursor_engineer=mysql.connection.cursor()
        query_cursor6=cursor_engineer.execute("SELECT * FROM ingenieur")
        if query_cursor6:
               all_engineers= cursor_engineer.fetchall()
               session["all_engineers"]=all_engineers
        if query:
            result= cursor.fetchall()
            if result:
                session["pm_logged"]=True
                session["pm_data"]=result
                cursor_projects_of_pm=mysql.connection.cursor()
                query_projects=cursor_projects_of_pm.execute("SELECT count(id_projet) FROM projet WHERE id_chef_trg=%s",(str(result[0][0])))
                # Enginners 
                cursor_eng_pm=mysql.connection.cursor()
                eng_query_pm=cursor_eng_pm.execute("SELECT count( DISTINCT id_ing) FROM tache JOIN projet on projet.id_projet=tache.id_projet JOIN chef_projet ON chef_projet.id_chef_prj=projet.id_chef_trg WHERE id_chef_prj=%s",(str(result[0][0])))
                if query_projects:
                    project_pm=cursor_projects_of_pm.fetchall() 
                    if project_pm:
                         session["project_pm"]=project_pm
                    if eng_query_pm:
                         engineers_pm=cursor_eng_pm.fetchall()
                         if engineers_pm:
                              session["engineers_en"]=engineers_pm

             # List Project of some enginner 
            project_cursor=mysql.connection.cursor()
            all_projects_query=project_cursor.execute("""SELECT projet.id_projet , projet.nom_projet ,ingenieur.nom_complet,status , projet.date_debut ,projet.date_fin FROM projet 
JOIN tache on tache.id_projet = projet.id_projet JOIN ingenieur on ingenieur.id_ing = tache.id_ing WHERE projet.id_chef_trg=%s""",(str(result[0][0])))
            if all_projects_query:
                 r_project=project_cursor.fetchall()
                 array_of_p=dictt(r_project)
               #   return redirect(url_for(".dashpm",projects=array_of_p)) 
                 session["data"]=array_of_p
            return redirect(url_for('dashpm')) 
                 
         

         




            # return redirect("/projectmanager-dash",302)
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

