import io
import base64
import matplotlib.pyplot as plt
import matplotlib.dates as mdates  # <-- добавь этот импорт
from django.shortcuts import render, get_object_or_404
from .models import City, WeatherRecord, ComfortRating


def home(request):
    cities = City.objects.all()
    return render(request, 'weather/home.html', {'cities': cities})


def city_detail(request, city_id):
    city = get_object_or_404(City, id=city_id)
    records = WeatherRecord.objects.filter(city=city).order_by('date')

    comfort_ratings = ComfortRating.objects.filter(city=city).order_by('date')
    comfort_dict = {cr.date: cr for cr in comfort_ratings}
    for record in records:
        record.comfort = comfort_dict.get(record.date)

    # --- Построение графика ---
    chart = None
    if records:
        dates = [r.date for r in records]
        temps = [r.temp for r in records]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, temps, marker='o', linestyle='-', color='b')
        plt.title(f'Температура в {city.name}')
        plt.xlabel('Дата')
        plt.ylabel('Температура (°C)')
        plt.grid(True)

        # --- Правильное форматирование дат ---
        # Устанавливаем формат: месяц, день, год
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%d %b %Y'))
        # Поворачиваем подписи для читаемости
        plt.gcf().autofmt_xdate()

        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        chart = base64.b64encode(buf.read()).decode('utf-8')
        buf.close()
        plt.close()

    return render(request, 'weather/city_detail.html', {
        'city': city,
        'records': records,
        'chart': chart,
    })