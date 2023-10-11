from flask import render_template, current_app, flash, redirect, url_for
from flask_login import current_user

from app.weather import weather
from app.weather.forms import CityForm
from utils.weather.city_weather import main as get_weather


@weather.route('/', methods=['GET', 'POST'])
def index():
    form = CityForm()
    if form.validate_on_submit():
        api_key = current_app.config['WEATHER_API_KEY']
        city_name = form.city_name.data
        city_weather = get_weather(city_name, api_key)

        if 'message' in city_weather:
            flash(city_weather['message'])
            return redirect(url_for('.index'))
        print(city_weather)

    return render_template(
        'weather/get_weather.html',
        title='Show weather info',
        form=form,
        city_weather = city_weather

    )
