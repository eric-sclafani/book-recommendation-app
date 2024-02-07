import sqlalchemy as sa
from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from src import db
from src.models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign in")


class RegistrationForm(FlaskForm):
    """
    Contains the registration code

    WTForms invokes the custom validate_<field_name> methods automatically
    """

    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        """Checks db if provided username already exists. If so, raise ValidationError"""
        query = sa.select(User).where(User.username == username.data)
        user = db.session.scalar(query)

        if user is not None:
            raise ValidationError(
                "That username is already taken. Please use a different username"
            )

    def validate_email(self, email):
        """Checks db if provided email already exists. If so, raise ValidationError"""
        query = sa.select(User).where(User.email == email.data)
        user = db.session.scalar(query)

        if user is not None:
            raise ValidationError("Account already exists for this email")
