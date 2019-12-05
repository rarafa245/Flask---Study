import os
import secrets
from PIL import Image
from app import app, bcrypt, db
from flask import render_template, url_for, flash, redirect
from .form import RegistrationForm, LoginForm, UpdateAccountForm
from app.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

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

@app.route("/posts")
def home():
    return render_template("home.html", posts=posts, title="Ola Mundo, Rafael")

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Your Acount Has Been Created !', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('register.html', title="Register", form=form)

@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Loggin Unsuccessful. Check Email ou Password!', 'danger')
    return render_template('login.html', title="Register", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profiles_pic', picture_fn)
    form_picture.save(picture_path)

    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():

        if form.picture.data:
            picture_file = save_picture(form.picture.data)

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.image_file = picture_file
        db.session.commit()
        flash('Your Account Has Been Updated!', 'success')
        return redirect(url_for('home'))
    image_file = url_for('static', filename='profiles_pic/' + current_user.image_file)
    return render_template('account.html', tittle='Account', image_file=image_file, form=form)
