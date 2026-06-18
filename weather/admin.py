from django.contrib import admin
from .models import City, WeatherRecord, ComfortRating

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'api_id')
    search_fields = ('name', 'country')

@admin.register(WeatherRecord)
class WeatherRecordAdmin(admin.ModelAdmin):
    list_display = ('city', 'date', 'temp', 'humidity', 'wind_speed')
    list_filter = ('city', 'date')
    search_fields = ('city__name',)

@admin.register(ComfortRating)
class ComfortRatingAdmin(admin.ModelAdmin):
    list_display = ('city', 'date', 'comfort_index', 'rating')
    list_filter = ('city', 'rating')
    search_fields = ('city__name',)