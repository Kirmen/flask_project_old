from flask_wtf import FlaskForm
from wtforms import SubmitField, HiddenField, StringField, IntegerField
from wtforms.validators import DataRequired, Length, Regexp, Email


class GenerateDataForm(FlaskForm):
    number = IntegerField('How many fake-users to generate:')
    submit = SubmitField('Generate')


class EditUserForm(FlaskForm):
    id = HiddenField()
    username = StringField(
        'Edit username',
        validators=[
            DataRequired(),
            Length(3, 100),
            Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must contains only letters, underscores or digits')
        ],
        render_kw={'placeholder': 'Enter your name'}
    )
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Length(10, 200),
            Email()
        ]
    )
    submit = SubmitField('Edit')


class CityWeather(FlaskForm):
    city = StringField('City')
    submit = SubmitField('Search weather')
