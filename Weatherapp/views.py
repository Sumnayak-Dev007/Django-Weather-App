import datetime
import requests
from django.shortcuts import render

def Home_view(request):
    API_KEY = '3a7e1a8a00ef3376db9a4e149460c0e7'
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    forecast_url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}"

    if request.method == "POST":
        city1 = request.POST['city1'].strip()  # Stripping city1 to remove any unwanted spaces
        city2 = request.POST.get('city2', None)

        weather_data1, daily_forecasts1 = fetch_weather_and_forecast(city1, API_KEY, current_weather_url, forecast_url)

        if city2:
            city2 = city2.strip() 
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
    print("Current Weather API Response:", response)   # DEBUG PRINT

    # If city not found or key invalid
    if response.get("cod") != 200:
        return {"error": response.get("message", "Unknown error")}, None

    lat = response["coord"]["lat"]
    lon = response["coord"]["lon"]

    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()
    print("Forecast API Response:", forecast_response)  # DEBUG PRINT

    weather_data = {
        'city': city,
        'temperature': round(response['main']['temp'] - 273.15, 2),
        'description': response['weather'][0]['description'],
        'icon': response['weather'][0]['icon'],
    }

    daily_forecasts = []
    for i in range(0, len(forecast_response.get('list', [])), 8):
        if len(daily_forecasts) >= 5:
            break
        f = forecast_response['list'][i]
        daily_forecasts.append({
            'day': datetime.datetime.fromtimestamp(f['dt']).strftime('%A'),
            'min_temp': round(f['main']['temp_min'] - 273.15, 2),
            'max_temp': round(f['main']['temp_max'] - 273.15, 2),
            'description': f['weather'][0]['description'],
            'icon': f['weather'][0]['icon'],
        })

    return weather_data, daily_forecasts
