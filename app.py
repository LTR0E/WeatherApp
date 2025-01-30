from flask import Flask, render_template, request
import requests
import time
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(city, country):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            return {
                'city': data['name'],
                'country': data['sys']['country'],
                'temp': data['main']['temp'],
                'desc': data['weather'][0]['description'].capitalize(),
                'wind': data['wind']['speed'],
                'humidity': data['main']['humidity'],
                'condition_id': data['weather'][0]['id']
            }
        return {'error': data.get('message', 'Error fetching weather data')}
    except requests.exceptions.RequestException as e:
        return {'error': str(e)}

def timeofday():
    hour = time.localtime().tm_hour
    if 5 <= hour < 12:
        return "nice morning"
    elif 12 <= hour < 18:
        return "nice afternoon"
    return "nice evening"

def get_weather_icon(condition_id):
    if 200 <= condition_id <= 232:
        return 'wi wi-thunderstorm'
    elif 300 <= condition_id <= 321:
        return 'wi wi-sprinkle'
    elif 500 <= condition_id <= 531:
        return 'wi wi-rain'
    elif 600 <= condition_id <= 622:
        return 'wi wi-snow'
    elif 701 <= condition_id <= 781:
        return 'wi wi-fog'
    elif condition_id == 800:
        return 'wi wi-day-sunny'
    elif condition_id == 801:
        return 'wi wi-day-cloudy'
    elif 802 <= condition_id <= 804:
        return 'wi wi-cloudy'
    else:
        return 'wi wi-alien'
    
@app.context_processor
def utility_processor():
    return dict(get_weather_icon=get_weather_icon)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form['city']
        country = request.form['country']
        weather_data = get_weather(city, country)
        return render_template('result.html', 
                             weather=weather_data,
                             timeofday=timeofday())
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))