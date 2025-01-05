import datetime
import requests
from django.shortcuts import render

def Home_view(request):
    API_KEY = 'ad277d69eb2aacf8dc4fa85cd556cd5e'
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}"

    if request.method == "POST":
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)

        weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, API_KEY, current_weather_url, forecast_url)

        if city2:
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, API_KEY, current_weather_url, forecast_url)
        else:
            weather_data2, daily_forecasts2 = None, None

        context = {
            'weather_data1': weather_data1,
            'daily_forecasts1': daily_forecasts1,
            'weather_data2': weather_data2,
            'daily_forecasts2': daily_forecasts2,
        }

        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')

def fetch_weather_and_forecast(city, api_key, current_weather_url, forecast_url):
    response = requests.get(current_weather_url.format(city, api_key)).json()
    lat, lon = response['coord']['lat'], response['coord']['lon']
    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()

    weather_data = {
        'city': city,
        'temperature': round(response['main']['temp'] - 273.15, 2),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }

    # Extracting the next 5 forecasts spaced roughly 24 hours apart
    daily_forecasts = []
    for i in range(0, len(forecast_response['list']), 8):  # 8 entries per day (3-hour intervals)
        if len(daily_forecasts) >= 5:
            break
        forecast = forecast_response['list'][i]
        daily_forecasts.append({
            'day': datetime.datetime.fromtimestamp(forecast['dt']).strftime('%A'),
            'min_temp': round(forecast['main']['temp_min'] - 273.15, 2),
            'max_temp': round(forecast['main']['temp_max'] - 273.15, 2),
            'description': forecast['weather'][0]['description'],
            'icon': forecast['weather'][0]['icon'],
        })

    return weather_data, daily_forecasts
