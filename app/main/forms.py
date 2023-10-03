from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class UserForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(3, 100)
        ],
        render_kw={
            'placeholder': 'Enter your name'}
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Length(10, 200),
            Email()
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            EqualTo('password_repeat', message='Password must match')
        ]
    )
    password_repeat = PasswordField(
        'Confirm password',
        validators=[DataRequired()]
    )
    submit = SubmitField(
        'Add user',
        render_kw={
            'class': 'btn btn-primary'
        }
    )
