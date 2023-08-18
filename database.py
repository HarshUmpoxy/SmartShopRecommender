# database.py
import mysql.connector
from flask_bcrypt import Bcrypt
from password import sql_password

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password=sql_password,
    database="smartshopusers"
)
cursor = db.cursor()

bcrypt = Bcrypt()

def create_table():
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (   
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(60),
        email VARCHAR(80),
        password VARCHAR(60)
    )
    """
    cursor.execute(create_table_query)

def insert_user(name, email, password):
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    insert_query = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    values = (name, email, hashed_password)

    cursor.execute(insert_query, values)
    db.commit()

def get_user_by_email(email):
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    return cursor.fetchall()
