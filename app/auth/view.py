from flask import flash, url_for, redirect, render_template

from . import auth
from .form import LoginForm, RegistrationForm
from ..model import Users, db
from ..email import send_email
from .. import login_manager
from flask_login import login_user, logout_user, login_required


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id)


@auth.route("/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=True)
            return redirect(url_for("education.get_topic_names"))
        else:
            flash("You entered incorrect email or password")
    return render_template("index.html", form=form, title="login", registration=True)


@auth.route("/registration", methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(form.user_name.data, form.password.data, form.email.data.lower())
        db.session.add(user)
        db.session.commit()
        send_email(form.email.data.lower(), "Welcome", user.id)
        return render_template("login.html", title="Check your email", content="Activation letter was sent to your "
                                                                               "email")
    return render_template("index.html", form=form, title="registration")


@auth.route("/users_verification/<uuid>")
def user_verification(uuid):
    user = Users.query.filter_by(id=uuid).first()
    login_user(user, remember=True)
    user.activate_user()
    return redirect(url_for("education.get_languages"))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for("auth.login"))
