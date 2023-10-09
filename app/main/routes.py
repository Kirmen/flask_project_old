from flask import render_template, flash, redirect, url_for, request, abort
from flask_login import current_user, login_required
from faker import Faker

from app import User, Profile, Role
from app.auth.utils import get_gravatar
from app.main import main
from app.main.forms import GenerateDataForm, EditUserForm, CityWeather
from app.main.utils import get_weather


@main.route('/', methods=['GET', 'POST'])
def index():
    form = GenerateDataForm()
    fake = Faker()
    number = form.number.data

    if number:
        for num in range(number):
            user_role = Role.select().where(Role.name == 'user').first()
            user_profile = Profile(
                avatar=get_gravatar(fake.email()),
                info=fake.name()
            )
            user_profile.save()
            user_role.save()

            user = User(
                username=fake.unique.first_name(),
                email=fake.email(),
                password='@dmiN1234',
                role=user_role,
                profile=user_profile
            )
            user.save()
            flash('fake-users has added')
            # if form.validate_on_submit():
            #     flash('Database filled with test data')
    return render_template(
        'main/index.html',
        title='Home page',
        form=form)



@main.route('/show/users')
@login_required
def show_users():
    """Show users information"""
    users = User.select()
    return render_template(
        'main/show_users.html',
        title='Show users',
        users=users)


@main.route('/edit/user/<int:user_id>', methods=['GET'])
@login_required
def edit_user(user_id: int):
    """Edit user"""
    if not current_user.is_admin():
        abort(403)

    user = User.select().where(User.id == user_id).first()
    if not user:
        abort(404)

    form = EditUserForm()
    form.id.label.text = ''
    form.id.data = user.id
    form.username.data = user.username
    form.email.data = user.email
    return render_template(
        'main/edit_user.html',
        title=f'Edit user {user.username}',
        form=form
    )


@main.route('/update/user', methods=['POST'])
@login_required
def update_user():
    form = EditUserForm()
    if form.validate_on_submit():
        user = User.get(User.id == int(form.id.data))
        user.username = form.username.data.strip().lower()
        user.email = form.email.data.strip().lower()
        user.save()
        flash(f'{user.username} updated')
    else:
        flash(form.errors)
    return redirect(url_for('.show_users'))


@main.route('/delete/users', methods=['POST'])
@login_required
def delete_users():
    """Delete selected users"""
    if not current_user.is_admin():
        flash('You don\'t have access to delete users', 'error')
        return redirect(url_for('.show_users'))

    selectors = list(map(int, request.form.getlist('selectors')))

    if current_user.id in selectors:
        flash('You can\'t delete yourself use profile page for this')
        return redirect(url_for('.show_users'))

    if not selectors:
        flash('Nothing to delete')
        return redirect(url_for('.show_users'))

    message = 'Deleted: '
    for selector in selectors:
        user = User.get(User.id == selector)
        profile = Profile.get(Profile.id == user.profile.id)
        message += f'{user.email} '
        user.delete_instance()
        profile.delete_instance()
    flash(message)
    return redirect(url_for('.show_users'))

@main.route('/weather', methods=['GET', 'POST'])
def weather():
    form=CityWeather()
    # flash('You have been logged out.')
    weather_condition = ''
    if form.city.data:
        WEATHER_API_KEY = 'cfd36353845324a3d7fee472955de516'
        OPENWEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={appId}&units=metric'

        weather_condition = get_weather(OPENWEATHER_API_URL,WEATHER_API_KEY, form.city.data)


    return render_template(
        'main/weather.html',
        title='Weather',
        form=form,
        weather_condition=weather_condition
    )
