from urllib.parse import urlsplit

import sqlalchemy as sa
from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from src import app, db
from src.forms import LoginForm, RegistrationForm
from src.models import User


@app.route("/")
@app.route("/index")
def index():
    """Home page of Flask Application."""
    posts = [
        {"author": {"username": "John"}, "body": "Beautiful day in Portland!"},
        {"author": {"username": "Susan"}, "body": "The Avengers movie was so cool!"},
    ]
    return render_template(
        "index.html",
        title="Home",
        posts=posts,
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)  # type: ignore
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        print("Congratulations, you are now a registered user!")
        return redirect(url_for("index"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    # if current user is already logged in, redirect them to index page
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        query = sa.select(User).where(User.username == form.username.data)
        user = db.session.scalar(query)

        if user is None or not user.check_password(form.password.data):
            print("Invalid username or password")
            return redirect(url_for("login"))

        login_user(user, remember=form.remember_me.data)

        # since the landing page has a login requirement, flask will attempt to redirect
        # the user after they've logged in to the page they requested to see
        # second conditional checks if user tries to inser a malicious URL in the 'next' argument
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)

    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


# <...> indicates a dynamic route. It will invoke the 'user' route function and pass the <...> text as an argument
@app.route("/user/<username>")
def user(username):
    query = sa.select(User).where(User.username == username)

    # if user is not found, automatically raises a 404 exception
    user = db.first_or_404(query)
    posts = [
        {"author": user, "body": "Test post #1"},
        {"author": user, "body": "Test post #2"},
    ]
    return render_template("user.html", user=user, posts=posts)
