from flask import render_template, request, url_for, flash, redirect
from mindful import app, db, bcrypt
from mindful.forms import RegistrationForm, LoginForm
from mindful.models import Client, User, Note
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/home")
@app.route("/")
def home():

    clients = Client.query.filter(Client.id > 10).limit(5)

    return render_template("home.html", clients=clients, help="help")


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/login", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f"unsuccessful login !", "danger")
        return redirect(url_for('home'))
    return render_template('login.html', title="login", form=form)


@app.route("/notes/<int:client_id>")
def notes(client_id):
    client = Client.query.get(client_id)
    notes = client.notes

    count = 0
    for note in notes:
        count += 1

    return render_template("notes.html", client=client, notes=notes, count=count)


@app.route("/logout")
def logout():
    logout_user()
    return render_template("home.html", title="Midful Practice'")
