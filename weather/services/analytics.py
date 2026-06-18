def calculate_comfort(temp, humidity, wind_speed):
    comfort = (temp - 20) - (wind_speed / 10) + (humidity / 100)
    if comfort > 5:
        rating = 'excellent'
    elif comfort > 0:
        rating = 'good'
    elif comfort > -5:
        rating = 'average'
    else:
        rating = 'poor'
    return comfort, rating