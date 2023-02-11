import requests
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = r'sqlite:///C:\Users\Maique\Desktop\social_network\weather.db'
db = SQLAlchemy(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
       new_city = request.form.get('city')
       if new_city:
        db.session.add(City(name=new_city))
        db.session.commit()
       
    cities = City.query.order_by(City.id.desc())
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=YOUR_KEY'

    weather_data = []

    for city in cities:
        r = requests.get(url.format(city.name)).json()

        weather = {
            'city': r['name'],
            'temp': round(r['main']['temp']),
            'desc': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
        weather_data.append(weather)
    return render_template('weather.html', weather_data=weather_data)


if __name__ == '__main__':
    app.run(debug=True)
