from flask import  Blueprint, render_template ,redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter(User.username.ilike(username)).first()

    if user is not None and check_password_hash(user.password, password):
        #success_message = f'Bienvenido { User.username }'
        #flash(success_message)
        login_user(user, remember= remember)
        return redirect(url_for('main.dashboard'))
    else:
        error_mesage = 'Usuario o contraseña no validos'
        flash(error_mesage)
        
    '''

    if not user and not check_password_hash(user.password,  password):
        flash('Revise los datos y vuelva a intentarlo')
        return redirect(url_for('auth.login'))
    '''
    return redirect(url_for('auth.login'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    

    user = User.query.filter(User.username.ilike(username)).first()
    user_email = User.query.filter(User.email.ilike(email)).first()

    if user:
        flash('El usuario ingredado ya existe.')
        return redirect( url_for('auth.signup'))

    if user_email:
        flash('La direccion de email ingresada ya existe.')
        return redirect( url_for('auth.signup'))

    new_user = User(email=email, username = username, password=generate_password_hash(password, method='sha256'))

    db.session.add(new_user)
    db.session.commit()

    return redirect( url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))



    