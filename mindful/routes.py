from flask import render_template, request, url_for, flash, redirect, request
from mindful import app, db, bcrypt
from mindful.forms import RegistrationForm, LoginForm, SearchForm, ClientUpdate, ClientNew, NoteForm, NewNote
from mindful.models import Client, User, Note
from flask_login import login_user, current_user, logout_user, login_required
from datetime import date


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
        return redirect(url_for("search"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('search'))
        else:
            flash("unsuccessful login! Check email and password.", "danger")
        return redirect(url_for('search'))
    return render_template('login.html', title="login", form=form)


@app.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()

    if request.method == 'POST':
        return search_results(form.first_name.data, form.last_name.data)
        # return render_template('search_results.html', client=client, title='results')
    else:
        client = Client
        return render_template('search.html', client=client, title='Seach', form=form)


@app.route("/note_list/<int:client_id>")
@login_required
def note_list(client_id):
    notes = Note.query.filter(Note.client_id == client_id).order_by(Note.note_date.desc()).all()
    client = Client.query.get(client_id)
    count = len(notes)
    return render_template('note_list.html', client=client, notes=notes, count=count, title='Notes')


@ app.route("/client/<int:id>", methods=['GET', 'POST'])
@ login_required
def clientinfo(id):
    form = ClientUpdate()    
    client = Client.query.get(id)
    if form.validate_on_submit():
        print("client")
        client.first_name = form.first_name.data
        client.last_name = form.last_name.data 
        client.street1 = form.street1.data 
        client.email = form.email.data 
        client.phone = form.phone.data 
        client.city = form.city.data 
        client.state = form.state.data 
        db.session.commit()
        flash("Update successful", "success")
        return redirect(url_for("clientinfo",id = client.id))
    notes = client.notes[-3:]
    form.first_name.data = client.first_name
    form.last_name.data = client.last_name
    form.street1.data = client.street1
    form.email.data = client.email
    form.phone.data = client.phone
    form.city.data = client.city
    form.state.data = client.state
    return render_template("client.html", client=client, notes=notes, form=form)
      


@ app.route("/client/new", methods=['GET', 'POST'])
@ login_required
def new_client():
    user=current_user
    form = ClientNew()
    client = Client
    legend = "New Client"
    if form.validate_on_submit():
        client = Client(first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        email=form.email.data,
                        phone=form.phone.data,
                        street1=form.street1.data,
                        city=form.city.data,
                        state=form.state.data,
                        user_id=current_user.id)
        db.session.add(client)
        db.session.commit()
        flash("new client created", "success")
        return redirect(url_for('clientinfo', id=client.id))

    return render_template("new_client.html", client=client, form=form, legend=legend)


@ app.route("/note/edit/<int:note_id>", methods=['GET','POST'])
@ login_required
def edit_session(note_id):
    form = NewNote()
    legend="Edit Session"
    note = Note.query.get_or_404(note_id)
    client = Client.query.get(note.client_id)
    # print(form.validate_on_submit())
    if form.validate_on_submit():
        note.description = form.description.data
        note.note_date = form.note_date.data
        db.session.commit()
        flash(note.description,"success")
        return redirect(url_for("clientinfo", id=note.client_id))
    form.note_date.data = note.note_date
    form.description.data = note.description
    return render_template("new_note.html", client=client, note=note, legend = legend, form=form, title="Edit session")



@ app.route("/note/new/<int:client_id>", methods=['GET', 'POST'])
@ login_required
def new_note(client_id):
    note=Note
    form = NewNote()
    # return render_template("new_note.html", note=note, form=form)
    client= Client.query.get(client_id)

    # print("here")
    note=Note
    legend = "New Note"
    if form.validate_on_submit():
        note = Note(description = form.description.data,
                note_date=form.note_date.data,
                client_id=client.id)
        db.session.add(note)
        db.session.commit()
        flash("new note created", "success")
        return redirect(url_for('clientinfo', id = client.id))
    elif request.method =='GET' :
        form.note_date.data = note.note_date.data = date.today() #.strftime("%d/%m/%Y")

    return render_template("new_note.html", note=note, form=form, client = client, legend=legend)


@ app.route("/search_results")
def search_results(first_name, last_name):
    clients = Client.query.filter(Client.first_name.like('%' + first_name + '%'),
                                  Client.last_name.like('%' + last_name + '%'), Client.user_id == current_user.id).all()
    return render_template('search_results.html', title="results", clients=clients)


@ app.route("/logout")
def logout():
    logout_user()
    return render_template("home.html", title="Midful Practice'")


@ app.route("/json", methods=['POST'])
def json():

    ppl = request.get_json()

    print(ppl)

    return "Got it", 200
