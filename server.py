from flask import Flask, render_template, request,url_for,redirect,session,flash
from flaskext.mysql import MySQL
from werkzeug import secure_filename


app = Flask(__name__)
mysql = MySQL()
mysql.init_app(app)

app.secret_key = 'any random string'
app.config["MYSQL_DATABASE_USER"] = "root"
app.config["MYSQL_DATABASE_PASSWORD"] = "mysql"
app.config["MYSQL_DATABASE_DB"] = "project"



@app.route('/')
def home_page():
	return render_template('index.html')

@app.route('/sign_up')
def sign_up():
   return render_template('signup.html')

@app.route('/login')
def login():
   return render_template('login.html')
   
@app.route('/logout')
def logout():
   session.pop('username',None)
   return redirect(url_for('login'))

@app.route('/mainpage')
def mainpage():
   return render_template('mainpage.html')


@app.route('/upload')
def upload_file():
   return render_template('home.html')
	
@app.route('/auth',methods = ['POST', 'GET'])
def authenticate():
   if request.method == 'POST':
      username = request.form['uname']
      password = request.form['pass']
      session['username'] = request.form['uname']
      if 'username' in session:
         username = session['username']
         
      conn = mysql.connect()
      cursor = mysql.get_db().cursor()
      sql1 = "select password from signup where username= %s";
      val1 = (username);
      db = cursor.execute(sql1,val1) 
      
      data = cursor.fetchall()
      for i,val in enumerate(data):
         print(i,val)
      if password == val[0]:
         if username != None:
            flash( 'Logged in as ' + username )
            return redirect(url_for('mainpage'))
      else:
         return 'false'
         
      mysql.get_db().commit()
      cursor.close()
      conn.close()
      
      
      
@app.route('/session')
def ses():
   if 'username' in session:
      username = session['username']
      return 'Logged in as ' + username + '<br>' + \
         "<b><a href = '/logout'>click here to log out</a></b>"
      return "You are not logged in <br><a href = '/login'></b>" + \
      "click here to log in</b></a>"


@app.route('/signupdb',methods=['POST','GET'])
def signupdb():
   if request.method == 'POST':
      fname = request.form['fname']
      lname = request.form['lname']
      username = request.form['uname']
      password = request.form['pass']
      rpassword = request.form['rpass']
      if password == rpassword:
         pwd = password

      conn = mysql.connect()
      cursor = mysql.get_db().cursor()
      sql = "insert into signup values(%s,%s,%s,%s)";
      val =(fname,lname,username,pwd);
      cursor.execute(sql,val)
      #cursor.execute("insert into signup (fname,lname,username,password) values({0},{1},{2},{3})".format(fname,lname,username,pwd));
     # sql1 = "select * from signup where username= (%s)";
      #val1 = (fname);
      #cursor.execute(sql,val) 

      #data = cursor.fetchall()
      mysql.get_db().commit()
      cursor.close()    
      conn.close()
      #for i,val in enumerate(data):
      #  print(i,val)
      return redirect(url_for('login'))
   else:
      return 'error'

@app.route('/uploader', methods = ['GET', 'POST'])
def upload():
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))
      return 'file uploaded successfully'
		
if __name__ == '__main__':
   app.run(debug = True)
