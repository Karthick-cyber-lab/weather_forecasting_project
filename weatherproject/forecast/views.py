from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import os
import requests
import pytz
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, accuracy_score
from datetime import datetime, timedelta
import os


API_KEY = '2f0c77c228f2c1d740b57f563655a57f'
BASE_URL = 'https://api.openweathermap.org/data/2.5/'


def get_current_weather(city):
    url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    return {
        "city": data["name"],
        "current_temp": round(data["main"]["temp"]),
        "humidity": round(data["main"]["humidity"]),
        "wind_speed": round(data["wind"]["speed"]),
        "description": data["weather"][0]["description"],
        "temp_min": round(data["main"]["temp_min"]),
        "temp_max": round(data["main"]["temp_max"]),
        "feels_like": round(data["main"]["feels_like"]),
        "pressure": round(data["main"]["pressure"]),
        "country": data["sys"]["country"],
        "Wind_gust_dir": data["wind"]["deg"],
        "Wind_Gust_Speed": data["wind"]["speed"],
        "clouds": data["clouds"]["all"],
        "visibility": data["visibility"]
    }


def read_historical_data(filename):
    df = pd.read_csv(filename)
    df = df.dropna()
    df = df.drop_duplicates()
    return df


def prepare_data(data):
    le = LabelEncoder()

    data["WindGustDir"] = le.fit_transform(data["WindGustDir"])
    data["RainTomorrow"] = le.fit_transform(data["RainTomorrow"])

    x = data[["MinTemp", "MaxTemp", "WindGustDir", "WindGustSpeed", "Humidity", "Pressure", "Temp"]]
    y = data["RainTomorrow"]

    return x, y, le


def train_rain_model(x, y):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=52)

    model = RandomForestClassifier(n_estimators=100, random_state=52)
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)

    print("RAIN MODEL MSE:", mean_squared_error(y_test, y_pred))
    print("ACCURACY:", accuracy_score(y_test, y_pred))

    return model


def prepare_regression_data(data, feature):
    x = []
    y = []

    for i in range(len(data) - 1):
        x.append(data[feature].iloc[i])
        y.append(data[feature].iloc[i + 1])

    x = np.array(x).reshape(-1, 1)
    y = np.array(y)

    return x, y


def train_regression_model(x, y):
    model = RandomForestRegressor(n_estimators=100, random_state=52)
    model.fit(x, y)
    return model


def predict_future(model, current_value):
    predictions = []
    value = current_value

    for i in range(5):
        value = model.predict([[value]])[0]
        predictions.append(value)

    return predictions


def weather_view(request):

    if request.method == "POST":

        city = request.POST.get("city")
        current_weather = get_current_weather(city)

        # Read weather.csv from the project directory (same folder as manage.py)
        csv_path = os.path.join(settings.BASE_DIR, "weather.csv")

        # Check if file exists
        if not os.path.exists(csv_path):
            return HttpResponse(f"weather.csv not found at:<br>{csv_path}")
        
        print("BASE_DIR =", settings.BASE_DIR)
        print("CSV PATH =", csv_path)
        print("FILE EXISTS =", os.path.exists(csv_path))

        historical_data = read_historical_data(csv_path)
        

        x, y, le = prepare_data(historical_data)

        rain_model = train_rain_model(x, y)

        wind_deg = current_weather["Wind_gust_dir"] % 360

        compass_points = [
            ("N", 0, 11.25), ("NNE", 11.25, 33.75), ("NE", 33.75, 56.25),
            ("ENE", 56.25, 78.75), ("E", 78.75, 101.25), ("ESE", 101.25, 123.75),
            ("SE", 123.75, 146.25), ("SSE", 146.25, 168.75), ("S", 168.75, 191.25),
            ("SSW", 191.25, 213.75), ("SW", 213.75, 236.25), ("WSW", 236.25, 258.75),
            ("W", 258.75, 281.25), ("WNW", 281.25, 303.75), ("NW", 303.75, 326.25),
            ("NNW", 326.25, 348.75)
        ]

        compass_direction = next(
            (point for point, start, end in compass_points if start <= wind_deg < end),
            "N"
        )

        if compass_direction in le.classes_:
            compass_direction_encoded = le.transform([compass_direction])[0]
        else:
            compass_direction_encoded = 0

        current_data = {
            "MinTemp": current_weather["temp_min"],
            "MaxTemp": current_weather["temp_max"],
            "WindGustDir": compass_direction_encoded,
            "WindGustSpeed": current_weather["Wind_Gust_Speed"],
            "Humidity": current_weather["humidity"],
            "Pressure": current_weather["pressure"],
            "Temp": current_weather["current_temp"],
        }

        current_df = pd.DataFrame([current_data])

        rain_prediction = rain_model.predict(current_df)[0]

        x_temp, y_temp = prepare_regression_data(historical_data, "Temp")
        x_hum, y_hum = prepare_regression_data(historical_data, "Humidity")

        temp_model = train_regression_model(x_temp, y_temp)
        hum_model = train_regression_model(x_hum, y_hum)

        future_temp = predict_future(temp_model, current_weather["temp_min"])
        future_hum = predict_future(hum_model, current_weather["humidity"])

        timezone = pytz.timezone("Asia/Kolkata")
        now = datetime.now(timezone)

        next_hour = now.replace(minute=0, second=0, microsecond=0)

        future_times = [
            (next_hour + timedelta(hours=i)).strftime("%H:00") for i in range(1, 6)
        ]

        time1, time2, time3, time4, time5 = future_times
        temp1, temp2, temp3, temp4, temp5 = future_temp
        hum1, hum2, hum3, hum4, hum5 = future_hum

        context = {

            "location": city,
            "current_temp": current_weather["current_temp"],
            "min_temp": current_weather["temp_min"],
            "max_temp": current_weather["temp_max"],
            "feels_like": current_weather["feels_like"],
            "clouds": current_weather["clouds"],
            "description": current_weather["description"],
            "city": current_weather["city"],
            "country": current_weather["country"],
            "time": datetime.now(),
            "date": datetime.now().strftime("%B %d, %Y"),
            "wind": current_weather["Wind_Gust_Speed"],
            "pressure": current_weather["pressure"],
            "visibility": current_weather["visibility"],

            "time1": time1,
            "time2": time2,
            "time3": time3,
            "time4": time4,
            "time5": time5,

            "temp1": f"{round(temp1,1)}",
            "temp2": f"{round(temp2,1)}",
            "temp3": f"{round(temp3,1)}",
            "temp4": f"{round(temp4,1)}",
            "temp5": f"{round(temp5,1)}",

            "hum1": f"{round(hum1,1)}",
            "hum2": f"{round(hum2,1)}",
            "hum3": f"{round(hum3,1)}",
            "hum4": f"{round(hum4,1)}",
            "hum5": f"{round(hum5,1)}",
        }

        return render(request, "weather.html", context)

    return render(request, "weather.html")