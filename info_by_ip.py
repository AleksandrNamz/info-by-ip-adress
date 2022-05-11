import requests
from openweather_key import api_key


def wind_info(dict):
    speed = round(dict['speed'])
    deg = round(dict['deg'])
    beaufort = ""
    orientation = ""

    # Check wind power
    beaufort_scale = {
        0: "calm", 1: "light air", 3: "light breeze", 5: "gentle breeze",
        7: "moderate breeze", 10: "fresh breeze", 12: "strong breeze", 15: "near gale",
        19: "gale", 23: "strong gale", 27: "storm", 31: "violent storm",
        32: "hurricane"
    }
    flag = True
    while flag:
        try:
            beaufort = beaufort_scale[speed]
            flag = False
        except KeyError:
            speed -= 1

    # Check wind orientation
    if 315 < deg <= 360 or 0 <= deg <= 45:
        orientation = "north"
    elif 45 < deg <= 135:
        orientation = "east"
    elif 135 < deg <= 225:
        orientation = "south"
    elif 225 < deg <= 315:
        orientation = "west"
    
    return f'{beaufort} ({round(dict["speed"])} m/s) from {orientation}'


def get_weather(lat=42.3667, lon=-88.0925):
    try:
        response_weather = requests.get(
            url=
            f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric'
        ).json()
        weather_data = {
            "[temperature]": round(response_weather['main']['temp']),
            "[feels like]": round(response_weather['main']['feels_like']),
            "[description]": response_weather['weather'][0]['description'],
            "[wind]": wind_info(response_weather['wind'])
        }
        print('-' * 30, '\n')
        print(' info about your local weather:')

        for key, value in  weather_data.items():
            print(f'{key} : {value}')

    except requests.exceptions.ConnectionError:
        print("проблемы с сервисом погоды")


def get_time(ip=None):
    try:
        time_response = requests.get(url=f'http://worldtimeapi.org/api/ip/{ip}').json()
        time_data = {
                "[current time]": time_response['datetime'][11:19],
                "[day of year]": time_response['day_of_year']
            }
        for key, value in time_data.items():
            print(f'{key} : {value}')

    except requests.exceptions.ConnectionError:
        print("возникли проблемы с сервисом точного времени.")


def get_ip(ip=None):
    try:
        response = requests.get(url=f'http://ip-api.com/json/{ip}').json()
        data = {
            "[ip]": response.get('query'),
            "[country]": response.get('country'),
            "[city]": response.get('city'),
            "[provider]": response.get('isp'),
        }
        print('\n', 'info about your location:')

        for key, value in data.items():
            print(f'{key} : {value}')

        get_time(ip=ip)

        print(f'[map] : https://www.google.com/maps/@{response.get("lat")},{response.get("lon")},15z')

        get_weather(lat=response.get("lat"), lon=response.get("lon"))

    except requests.exceptions.ConnectionError:
        print('возникли проблемы с соединением.')


def main(ip=None):
    ip = input('enter target ip:')

    get_ip(ip=ip)


if __name__ == '__main__':
    main()