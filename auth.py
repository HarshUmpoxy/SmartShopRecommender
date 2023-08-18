# auth.py
from flask import Blueprint, render_template, request, redirect, session
from database import insert_user, get_user_by_email, bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = get_user_by_email(email)
    
    if user and bcrypt.check_password_hash(user[0][3], password):
        session['user_id'] = user[0][0]
        return redirect('/')
    else:
        return redirect('/login')
