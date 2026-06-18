import requests
from datetime import datetime
from django.conf import settings
from weather.models import City, WeatherRecord, ComfortRating
from .analytics import calculate_comfort

API_KEY = settings.OPENWEATHER_API_KEY
BASE_URL = "http://api.openweathermap.org/data/2.5/forecast"


def get_weather_data(city_api_id):
    params = {
        'id': city_api_id,
        'appid': API_KEY,
        'units': 'metric',
        'lang': 'ru'
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        result = []
        for item in data['list']:
            dt = datetime.fromtimestamp(item['dt'])
            result.append({
                'date': dt.date(),
                'temp': item['main']['temp'],
                'humidity': item['main']['humidity'],
                'wind_speed': item['wind']['speed'],
                'description': item['weather'][0]['description'],
            })
        return result
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return None


def update_weather_for_city(city):
    data = get_weather_data(city.api_id)
    if not data:
        return False

    for entry in data:
        # Сохраняем запись погоды
        record, created = WeatherRecord.objects.update_or_create(
            city=city,
            date=entry['date'],
            defaults={
                'temp': entry['temp'],
                'humidity': entry['humidity'],
                'wind_speed': entry['wind_speed'],
                'description': entry['description'],
            }
        )
        # Рассчитываем комфорт
        comfort_index, rating = calculate_comfort(
            entry['temp'],
            entry['humidity'],
            entry['wind_speed']
        )
        # Сохраняем комфорт
        ComfortRating.objects.update_or_create(
            weather_record=record,
            defaults={
                'city': city,
                'date': entry['date'],
                'comfort_index': comfort_index,
                'rating': rating,
            }
        )
    return True