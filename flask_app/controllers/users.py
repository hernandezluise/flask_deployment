from flask_app import app
from flask import redirect, render_template, session, request, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

# creates new user/validates

@app.route('/users/create', methods=["POST"])
def create_user():
    if not User.validate_user(request.form):
        return redirect('/')
    password_hash = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": password_hash
    }
    print(password_hash)
    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect('/home')

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('home.html', user = User.get_user(data))

@app.route('/login', methods=["POST"])
def login():
    user = User.get_email(request.form)
    user_password = request.form['password']
    if not user:
        flash("Invalid email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, user_password):
        flash("Invalid Password", "login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/home')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')