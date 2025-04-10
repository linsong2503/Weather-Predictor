from django.shortcuts import render

from django.http import HttpResponse

import requests
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from datetime import datetime, timedelta
import pytz
import os

API_KEY = "0f7760dac2ea98d33292d55204228766"
BASE_URL = "https://api.openweathermap.org/data/2.5/"

# Get features from API


def get_current_weather(city):
    url = f"{BASE_URL}weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    return {
        "city": data["name"],
        "current_temp": round(data["main"]["temp"]),
        "feels_like": round(data["main"]["feels_like"]),
        "temp_min": round(data["main"]["temp_min"]),
        "temp_max": round(data["main"]["temp_max"]),
        "humidity": round(data["main"]["humidity"]),
        "description": data["weather"][0]["description"],
        "pressure": data["main"]["pressure"],
        "country": data["sys"]["country"],
        "wind_gust_dir": data["wind"]["deg"],
        "WindGustSpeed": data["wind"]["speed"],
        "clouds": data["clouds"]["all"],
        "visibility": data["visibility"],
    }

    # read csv file


def read_data(file):
    df = pd.read_csv(file)
    df.dropna()
    df.drop_duplicates()
    return df


# Encode data


def prepare_data(data):
    le = LabelEncoder()
    data["WindGustDir"] = le.fit_transform(data["WindGustDir"])
    data["RainTomorrow"] = le.fit_transform(data["RainTomorrow"])

    X = data[
        [
            "MinTemp",
            "MaxTemp",
            "WindGustDir",
            "WindGustSpeed",
            "Humidity",
            "Pressure",
            "Temp",
        ]
    ]
    y = data["RainTomorrow"]
    return X, y, le


# Train rain model


def train_rain_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_predicted = model.predict(X_test)
    # print(mean_squared_error(y_test, y_predicted))
    return model


# Iterate through features in dataset. Turn them into arrays


def prepare_regression_data(data, feature):
    X, y = [], []
    for i in range(len(data) - 1):
        X.append(data[feature].iloc[i])
        y.append(data[feature].iloc[i + 1])
    X = np.array(X).reshape(-1, 1)
    y = np.array(X)
    return X, y


def train_regression_model(X, y):
    model = RandomForestRegressor(random_state=42, n_estimators=100)
    model.fit(X, y)
    return model


# Give prediction about rain, temperature and humidity, etc...


def predict_value(model, current_value):
    prediction = [current_value]
    for i in range(5):
        next_value = model.predict([[prediction[-1]]])
        prediction.append(next_value[0])
    return prediction[1:]


def weather_view(request):
    if request.method == "POST":
        
            city = request.POST.get("city")
            current_weather = get_current_weather(city)
            csv_path = os.path.join(
                "C:\\Users\\OS\\OneDrive\\Desktop\\WPP\\weatherProject\\weather.csv"
            )
            historical_data = read_data(csv_path)

            X, y, le = prepare_data(historical_data)
            rain_model = train_rain_model(X, y)

            # Convert wind direction from directions to degree based on compass points

            wind_deg = current_weather["wind_gust_dir"] % 360

            compass_points = [
                ("N", 0, 11.25),
                ("NNE", 11.25, 33.75),
                ("NE", 33.75, 56.25),
                ("ENE", 56.25, 78.75),
                ("E", 78.75, 101.25),
                ("ESE", 101.25, 123.75),
                ("SE", 123.75, 146.25),
                ("SSE", 146.25, 168.75),
                ("S", 168.75, 191.25),
                ("SSW", 191.25, 213.75),
                ("SW", 213.75, 236.25),
                ("WSW", 236.25, 258.75),
                ("W", 258.75, 281.25),
                ("WNW", 281.25, 303.75),
                ("NW", 303.75, 326.25),
                ("NNW", 326.25, 348.75),
            ]
            compass_direction = next(
                points for points, start, end in compass_points if start <= wind_deg < end
            )
            compass_directions_encoded = (
                le.transform([compass_direction])[0]
                if compass_direction in le.classes_
                else -1
            )

            current_data = {
                "MinTemp": current_weather["temp_min"],
                "MaxTemp": current_weather["temp_max"],
                "WindGustDir": compass_directions_encoded,
                "WindGustSpeed": current_weather["WindGustSpeed"],
                "Humidity": current_weather["humidity"],
                "Pressure": current_weather["pressure"],
                "Temp": current_weather["current_temp"],
            }

            current_df = pd.DataFrame([current_data])

            rain_prediction = rain_model.predict(current_df)[0]
            X_temp, y_temp = prepare_regression_data(historical_data, "Temp")
            X_hum, y_hum = prepare_regression_data(historical_data, "Humidity")

            temp_model = train_regression_model(X_temp, y_temp)
            hum_model = train_regression_model(X_hum, y_hum)

            future_temp = predict_value(temp_model, current_weather["temp_min"])
            future_hum = predict_value(hum_model, current_weather["humidity"])

            # Set time for prediction

            timezone = pytz.timezone("Asia/Ho_Chi_Minh")
            now = datetime.now(timezone)
            next_hour = now + timedelta(hours=1)
            next_hour = next_hour.replace(minute=0, second=0)
            future_times = [
                (next_hour + timedelta(hours=i)).strftime("%H:00") for i in range(5)
            ]

            time1, time2, time3, time4, time5 = future_times
            temp1, temp2, temp3, temp4, temp5 = future_temp
            hum1, hum2, hum3, hum4, hum5 = future_hum

            # Pass data

            context = {
                "location": city,
                "current_temp": current_weather["current_temp"],
                "MinTemp": current_weather["temp_min"],
                "MaxTemp": current_weather["temp_max"],
                "feels_like": current_weather["feels_like"],
                "humidity": current_weather["humidity"],
                "clouds": current_weather["clouds"],
                "description": current_weather["description"],
                "city": current_weather["city"],
                "country": current_weather["country"],
                "time": datetime.now(),
                "date": datetime.now().strftime("%B $d, %Y"),
                "wind": current_weather["WindGustSpeed"],
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

# def weather_view():
#   city = input("Enter city name: ")
#   current_weather = get_current_weather(city)
#   csv_path = os.path.join(
#           "C:\\Users\\OS\\OneDrive\\Desktop\\WPP\\weatherProject\\weather.csv"
#         )
#   historical_data = read_data(csv_path)

#   X,y,le = prepare_data(historical_data)
#   rain_model = train_rain_model(X,y)

#   wind_deg = current_weather['wind_gust_dir'] % 360

#   compass_points = [("N",0,11.25),("NNE",11.25,33.75),("NE",33.75,56.25),
#                     ("ENE",56.25,78.75),("E",78.75,101.25),("ESE",101.25,123.75),
#                     ("SE",123.75,146.25),("SSE",146.25,168.75),("S",168.75,191.25),
#                     ("SSW",191.25,213.75),("SW",213.75,236.25),("WSW",236.25,258.75),
#                     ("W",258.75,281.25),("WNW",281.25,303.75),("NW",303.75,326.25),
#                     ("NNW",326.25,348.75)
#                     ]
#   compass_direction = next(points for points,start,end in compass_points if start<=wind_deg<end)
#   compass_directions_encoded = le.transform([compass_direction])[0] if compass_direction in le.classes_ else -1

#   current_data = {
#       'MinTemp' : current_weather['temp_min'],
#       'MaxTemp' : current_weather['temp_max'],
#       'WindGustDir': compass_directions_encoded,
#       'WindGustSpeed' : current_weather['WindGustSpeed'],
#       'Humidity': current_weather['humidity'],
#       'Pressure': current_weather['pressure'],
#       'Temp' : current_weather['current_temp']
#   }

#   current_df = pd.DataFrame([current_data])

#   rain_prediction = rain_model.predict(current_df)[0]
#   X_temp,y_temp = prepare_regression_data(historical_data,"Temp")
#   X_hum,y_hum = prepare_regression_data(historical_data,"Humidity")

#   temp_model = train_regression_model(X_temp,y_temp)
#   hum_model = train_regression_model(X_hum,y_hum)

#   future_temp = predict_value(temp_model,current_weather['temp_min'])
#   future_hum = predict_value(hum_model,current_weather['humidity'])

#   timezone = pytz.timezone('Asia/Ho_Chi_Minh')
#   now = datetime.now(timezone)
#   next_hour = now + timedelta(hours=1)
#   next_hour = next_hour.replace(minute=0,second=0)
#   future_times = [(next_hour+timedelta(hours=i)).strftime("%H:00") for i in range(10)]


#   print(f"City:{city}, {current_weather['country']} ")

#   print(f"Current temperature:{current_weather['current_temp']}")
#   print(f"Feels like:{current_weather['feels_like']}")
#   print(f"Minimum temperature:{current_weather['temp_min']}")
#   print(f"Maximum temperature:{current_weather['temp_max']}")
#   print(f"Humidity:{current_weather['humidity']}")
#   print(f"Pressure:{current_weather['pressure']}")
#   print(f"Wind Gust Direction:{current_weather['wind_gust_dir']}")
#   print(f"Wind Gust Speed:{current_weather['WindGustSpeed']}")
#   print(f"Prediction:{current_weather['description']}")
#   print(f"Rain Prediction:{'Yes' if rain_prediction else 'No'}")
#   print()
#   print("Future Temperature Prediction ","\n")
#   for time, temp in zip(future_times,future_temp):
#     print(f"Time:{time}, Temp:{temp}")
#   print()
#   print("Future Humidity Prediction ","\n")
#   for time, hum in zip(future_times,future_hum):
#     print(f"Time:{time}, Temp:{hum}")


# weather_view()