from app import app, bcrypt, db
from flask import render_template, url_for, flash, redirect
from .form import RegistrationForm, LoginForm
from app.models import User, Post
from flask_login import login_user

posts = [
    {
        'autor' : 'Rafael R Ferreira',
        'title' : 'Blog Post 1',
        'content' : 'First Post Content',
        'date_posted' : 'November 30, 2019'
    },
    {
        'autor' : 'Isabela B Teixeira Cataldo',
        'title' : 'Blog Post 2',
        'content' : 'Second Post Content',
        'date_posted' : 'December 1, 2019'
    }

]

@app.route("/")
def home():
    return render_template("home.html", posts=posts, title="Ola Mundo, Rafael")

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Your Acount Has Been Created !', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('register.html', title="Register", form=form)

@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Loggin Unsuccessful. Check Email ou Password!', 'danger')
    return render_template('login.html', title="Register", form=form)