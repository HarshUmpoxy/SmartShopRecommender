import os
from flask import Flask, session, redirect, render_template, request
from auth import auth_bp
from database import create_table, get_user_by_email, insert_user
from BooksRecommendorSystem.app import books_bp
from fashion.app import fashion_bp
from admin.app import admin_blueprint
from Electronics.app import electronics_bp
app = Flask(__name__)
app.secret_key = os.urandom(24)

#registering all the necessary blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(books_bp, url_prefix='/books')  
app.register_blueprint(fashion_bp, url_prefix='/fashion')
app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(electronics_bp, url_prefix='/electronics')

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

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')

    insert_user(name, email, password)
    
    user = get_user_by_email(email)
    session['user_id'] = user[0][0]
    
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/login')

def create_app():
    return app

if __name__ == "__main__":
    app = create_app()
    create_table()  # Create the database table
    app.run(debug=True)
