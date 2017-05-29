from flask import render_template, request, flash, redirect, url_for
from flask.ext.login import login_user

from app import app, login_manager
from forms import LoginForm

@app.route('/')
def homepage():
    name = request.args.get('name')
    number = request.args.get('number')
    # Pass name into the template context
    return render_template('homepage.html', name=name, number=number)
    
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form = LoginForm(request.form)
        # The user is validated and authenticated.
        if form.validate():
            # login_user handles setting the correct session values.
            login_user(form.user, remember=form.remember_me.data)
            flash("Successfully logged in as {}.".format(form.user.email), 
                  "success")
            return redirect(request.args.get("next") or url_for("homepage"))
    else:
        form = LoginForm()
    return render_template("login.html", form=form)