from flask import render_template, flash, redirect, url_for

from app.main import main
from app.main.models import User, Role, Profile
from app.main.forms import UserForm


@main.route('/')
def index():
    form = UserForm()
    return render_template(
        'main/index.html',
        title='Home page',
        form=form,
    )


@main.route('/add/user/', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        user_role = Role.select().where(Role.name == 'user').first()
        user_profile = Profile(
            avatar='cat.png'
        )
        user_profile.save()

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            role=user_role,
            profile=user_profile
        )

        user.save()
        flash(f'{user.username} has added')
    return redirect(url_for('.index'))
