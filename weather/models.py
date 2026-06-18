from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название города")
    country = models.CharField(max_length=100, verbose_name="Страна")
    api_id = models.IntegerField(unique=True, verbose_name="ID в OpenWeather")

    def __str__(self):
        return f"{self.name}, {self.country}"

class WeatherRecord(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='weather_records')
    date = models.DateField(verbose_name="Дата прогноза")
    temp = models.FloatField(verbose_name="Температура (°C)")
    humidity = models.IntegerField(verbose_name="Влажность (%)")
    wind_speed = models.FloatField(verbose_name="Скорость ветра (м/с)")
    description = models.CharField(max_length=200, verbose_name="Описание погоды")

    class Meta:
        unique_together = ('city', 'date')
        ordering = ['date']

    def __str__(self):
        return f"{self.city.name} – {self.date}"

class ComfortRating(models.Model):
    RATING_CHOICES = [
        ('excellent', 'Отлично'),
        ('good', 'Хорошо'),
        ('average', 'Средне'),
        ('poor', 'Плохо'),
    ]

    weather_record = models.OneToOneField(
        WeatherRecord,
        on_delete=models.CASCADE,
        related_name='comfort',
        verbose_name="Запись погоды"
    )
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        verbose_name="Город"
    )
    date = models.DateField(verbose_name="Дата")
    comfort_index = models.FloatField(verbose_name="Индекс комфорта")
    rating = models.CharField(
        max_length=20,
        choices=RATING_CHOICES,
        verbose_name="Оценка"
    )

    class Meta:
        unique_together = ('city', 'date')  # чтобы не было дублей
        ordering = ['date']

    def __str__(self):
        return f"{self.city.name} – {self.date}: {self.comfort_index:.2f} ({self.get_rating_display()})"