#Rotas
from flask import render_template, url_for, flash, redirect
from app import app
from .form import RegistrationForm, LoginForm

app.config['SECRET_KEY'] = '123'

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
        flash(f'Acount created for {form.username.data} !', 'success')
        return redirect(url_for('home'))
    else:
        return render_template('register.html', title="Register", form=form)

@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "rafael@logpyx.com" and form.password.data == "128Parsecs!":
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Loggin Unsuccessful. Check Email ou Password!', 'danger')
            return redirect(url_for('home'))
    return render_template('login.html', title="Register", form=form)