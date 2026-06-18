from django.core.management.base import BaseCommand
from weather.models import City
from weather.services.weather_api import update_weather_for_city

class Command(BaseCommand):
    help = 'Обновляет погоду для всех городов в базе'

    def handle(self, *args, **options):
        cities = City.objects.all()
        if not cities:
            self.stdout.write(self.style.WARNING('Нет городов в базе.'))
            return

        success_count = 0
        for city in cities:
            self.stdout.write(f'Обновление погоды для {city.name}...')
            if update_weather_for_city(city):
                success_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✅ {city.name} обновлён'))
            else:
                self.stdout.write(self.style.ERROR(f'  ❌ Ошибка при обновлении {city.name}'))

        self.stdout.write(self.style.SUCCESS(f'\n✅ Успешно обновлено {success_count} из {cities.count()} городов.'))