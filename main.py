from flask import Flask, render_template, request, redirect, session
import mysql.connector
import os
from password import sql_password

app=Flask(__name__)
app.secret_key=os.urandom(24)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=sql_password,
    database="smartshopusers"
)
cursor = db.cursor()
create_table_query = """
CREATE TABLE IF NOT EXISTS users (   
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(60),
    email VARCHAR(80),
    password VARCHAR(60)
)
"""
cursor.execute(create_table_query)


@app.route('/')
def home():
    if 'user_id' in session:
        return render_template('index.html')
    else:
        return redirect('/login')

@app.route('/login')
def login():
    if 'user_id' in session:
        return render_template('index.html')
    else:
        return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')
    # print(email)
    # print(password)
    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email, password))
    users=cursor.fetchall()
    if(len(users) > 0):
        session['user_id']=users[0][0]
        return redirect('/')
    else:
        return redirect('/login')


@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')

    insert_query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    values = (name, email, password)

    cursor.execute(insert_query, values)
    db.commit()

    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
    myuser=cursor.fetchall()
    session['user_id']=myuser[0][0]
    return redirect('/')  
    
@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/login')

if __name__=="__main__":
    app.run(debug=True)