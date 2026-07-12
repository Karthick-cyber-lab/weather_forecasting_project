# 🌦️ Real-Time Weather Forecasting Website with Django & Machine Learning

This project is a **Real-Time Weather Forecasting Web Application** built using **Django, Python, and Machine Learning**.
It predicts weather conditions and rainfall probability based on historical weather data and displays the results in a web dashboard.

---

## 📌 Features

* Real-time weather data display
* Rain prediction using Machine Learning
* Temperature visualization using charts
* Clean weather dashboard UI
* Django backend with ML model integration
* Uses historical weather dataset (`weather.csv`)

---

## 🛠️ Technologies Used

* Python
* Django
* Machine Learning (Scikit-learn)
* Pandas
* NumPy
* Chart.js
* HTML / CSS / JavaScript

---

## 📂 Project Structure

```
ML_PROJECT
│
├── weatherproject
│   ├── views.py
│   ├── settings.py
│   ├── templates
│   │   └── weather.html
│   └── static
│       ├── css
│       │   └── styles.css
│       └── js
│           └── chartSetup.js
│
├── weather.csv
├── manage.py
└── venv
```

---

## ⚙️ Installation Guide

### 1️⃣ Install Python and VS Code

Download and install:

* Python
* Visual Studio Code


open this web and create api -- https://openweathermap.org › api ----replace it in views.py  (it will take 2 hrs)
---

### 2️⃣ Open Terminal in VS Code

Press:

```
Ctrl + Shift + ~
```

---

### 3️⃣ Create Virtual Environment

```
python -m venv venv
```

---

### 4️⃣ Activate Virtual Environment

For **Windows**

```
.\venv\Scripts\activate
```

For **Mac / Linux**

```
source venv/bin/activate
```

---

### 5️⃣ Install Required Libraries

```
pip install django pandas numpy scikit-learn requests
```

---

### 6️⃣ Run the Django Server

Navigate to project folder and run:


cd .\weatherproject\   

```
python manage.py runserver
```

---

### 7️⃣ Open in Browser

```
http://127.0.0.1:8000
```

---

## 📊 Machine Learning Model

The system trains a **Random Forest model** using historical weather data to predict rainfall probability.

Evaluation metrics printed in terminal:

* Accuracy
* Mean Squared Error (MSE)

---

## 📈 Visualization

Weather temperature trends are displayed using **Chart.js line graphs**.

---


Machine Learning Project – Weather Forecasting System

---

