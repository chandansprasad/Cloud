from flask import Flask, render_template, redirect, url_for, request, json
from flaskext.mysql import MySQL
from werkzeug import secure_filename
from collections import Counter
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/home/ubuntu/flaskapp/uploads' 

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'ubuntu'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ubuntu'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
mysql = MySQL(app)


@app.route("/")
def index():
    return render_template('index2.html')



@app.route('/signupbtn', methods=['POST'])
def signupbtn():
    return render_template('signup.html')

@app.route('/signUp',methods=['GET','POST'])
def signUp():
    
    success = 'User signed up. Please Login.'
    # read the posted values from the UI
    fname = request.form['inputfName']
    lname = request.form['inputlName']
    email = request.form['inputEmail']
    password = request.form['inputPassword']
    username = request.form['inputEmail']
    

    conn = mysql.connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO userslist(username, password, fname, lname, email) VALUES (%s, %s, %s, %s, %s)", (username, password, fname , lname, email))
    conn.commit()
    cur.close()
    conn.close()
    return render_template('index2.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    conn = mysql.connect()
    cursor = conn.cursor()
    userName = request.form['uname']
    password = request.form['psw']
    query = ("SELECT * FROM userslist WHERE username = %s")
    cursor.execute(query,userName)
    data = cursor.fetchall()
    if len(data) is 0:
        return render_template('index2.html', error = 'User Name not found. Please sign up as a new user.')
    dbPassword = data[0][1]
    firstName = data[0][2]
    lastName = data[0][3]
    email = data[0][4]
    cursor.close()
    conn.close()
    if request.method == 'POST':
        if password == dbPassword:
                
	    return render_template('welcome.html',fName=firstName, lName=lastName, email=email) 

        else:
    	    return render_template('index2.html', error = 'Invalid Credentials. Please try again.') 


@app.route('/uploader', methods = ['GET','POST'])
def uploader():

   if request.method == 'POST':
      f = request.files['file']
      if f.filename == '':
         return redirect(request.url)
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))

      with open(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)), 'r') as file:
         data = file.read().replace('\n', '')

      input_counter = Counter(data)
      response = []
      for letter, count in input_counter.most_common():
          response.append('"{}": {}'.format(letter, count))
      return '<br>'.join(response)

   return 'Please go back and choose a file before submitting'


if __name__ == "__main__":
	app.run(debug='True')


