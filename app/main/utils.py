import requests

WEATHER_API_KEY = 'cfd36353845324a3d7fee472955de516'
OPENWEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={appId}&units=metric'

COLD = 'Cold'
NORMAL = 'Normal'
WARM = 'Warm'
HOT = 'Hot'


def get_weather(weather_url: str, api_key: str, city: str):
    """
    @param str weather_url: Parametrized openweather url
    @param api_key: Api key
    @param city: City name
    @return str: Weather condition

    Reference: https://openweathermap.org/current
    """
    weather_condition = ''
    url = weather_url.format(
        city=city,
        appId=api_key
    )

    response = requests.get(url)
    if response.status_code != 200:
        message = 'openweathermap.org returned non-200 code. Actual code is {code}, message is: {message}'.format(
            code=str(response.status_code),
            message=response.json()['message']
        )
        raise RuntimeError(message)

    temperature = response.json()['main']['temp']

    if temperature < 10:
        weather_condition = COLD
    elif temperature < 20:
        weather_condition = NORMAL
    elif temperature < 25:
        weather_condition = WARM
    else:
        weather_condition = HOT
    return f'In {city} it is {weather_condition}, {temperature=}'


# if __name__ == '__main__':
#     print(get_weather(OPENWEATHER_API_URL, WEATHER_API_KEY, 'Barcelona'))