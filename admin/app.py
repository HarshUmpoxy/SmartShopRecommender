from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint
from passlib.hash import pbkdf2_sha256
import mysql.connector
from password import sql_password

# Create the admin blueprint
admin_blueprint = Blueprint('admin_blueprint', __name__, static_folder='static', template_folder='templates')

print("admin is called")

# Database connection setup
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password=sql_password,
    database='smartshopusers'
)

# Create the admin_users table
def create_admin_users_table():
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admin_users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            role VARCHAR(50) NOT NULL
        )
    """)
    db.commit()
    cursor.close()

def is_admin(username):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT role FROM admin_users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    return user and user['role'] == 'admin'

@admin_blueprint.route('/')
def admin_index():
    print("inside /admin...................#####....")
    # print({{url_for(admin_blueprint.admin_login)}})
    return render_template('admin_index.html')
    # return redirect(url_for('admin_blueprint.admin_login'))


@admin_blueprint.route('/register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = pbkdf2_sha256.hash(password)
        
        cursor = db.cursor()
        cursor.execute("INSERT INTO admin_users (username, password, role) VALUES (%s, %s, %s)", (username, hashed_password, 'admin'))
        db.commit()
        cursor.close()

        flash('Registration successful. Please log in.', 'success')
        return render_template('admin_index.html')

    return render_template('admin_register.html')

@admin_blueprint.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print("username", username)
        print("password", password)
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT password FROM admin_users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        
        if user and pbkdf2_sha256.verify(password, user['password']):
            session['username'] = username
            return render_template('admin_dashboard.html')
        print("Incorrect Credentials of admin")
        flash('Invalid username or password', 'error')

    return render_template('admin_login.html')

@admin_blueprint.route('/dashboard')
def admin_dashboard():
    if 'username' in session and is_admin(session['username']):
        return render_template('admin_dashboard.html')

    flash('Access denied', 'error')
    return redirect('/admin/login')

@admin_blueprint.route('/report_dashboard')
def report_dashboard():
    if 'username' in session and is_admin(session['username']):
        return render_template('report_dashboard.html')

    flash('Access denied', 'error')
    return redirect('/admin/login')

@admin_blueprint.route('/logout')
def admin_logout():
    session.pop('username', None)
    return redirect('/admin')

# if __name__ == '__main__':
#     create_admin_users_table()  # Create the admin_users table if it doesn't exist
#     app.run(debug=True)
