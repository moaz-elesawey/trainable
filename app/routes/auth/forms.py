from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
)
from wtforms.validators import DataRequired, Length, EqualTo


empty_option = [("", "-------")]


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=4, max=25)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=50)]
    )
    remember = BooleanField("Remember Me", default=True)

    submit = SubmitField("Sign in")


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(
        "Old Password", validators=[DataRequired(), Length(min=8, max=50)]
    )
    new_password = PasswordField(
        "New Password", validators=[DataRequired(), Length(min=8, max=50)]
    )
    new_password_confirm = PasswordField(
        "New Password Confirm",
        validators=[DataRequired(), Length(min=8, max=50), EqualTo("new_password")],
    )

    submit = SubmitField("Change")
