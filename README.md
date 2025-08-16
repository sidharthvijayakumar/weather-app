# weather-app
# Weather Dashboard Web Application

## Project Overview
This is a simple Flask-based web application that displays weather information for a given city. The application fetches real-time weather data using a public weather API and is hosted on an Amazon EC2 instance.

## Tech Stack
- **Backend:** Python (Flask)
- **Frontend:** HTML, CSS (Bootstrap)
- **API:** OpenWeatherMap API (or any free weather API)
- **Server:** Amazon EC2 (Ubuntu/Windows)
- **Deployment Tools:** Gunicorn, Nginx (optional)

## Features
- Fetches and displays current weather for a given city
- Simple and responsive UI
- Hosted on an AWS EC2 instance for accessibility

## Installation and Setup

### 1. Clone the Repository
```sh
mkdir weather-app && cd weather-app
```

### 2. Install Dependencies
Create a `requirements.txt` file with the following:
```txt
Flask
requests
logging
gunicorn
```
Then install dependencies:
```sh
pip install -r requirements.txt
```

### 3. Create the Flask App (app.py)
```python
from flask import Flask, render_template, request
import requests
import logging
from requests.exceptions import ConnectTimeout, HTTPError

# Logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Config
API_KEY = ""  # Replace with your actual API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def home():
    weather = None
    error = None
    if request.method == "POST":
        city = request.form.get("city")
    elif request.method == "GET":
        city = request.args.get("city", "kochi") #default city
    if city:
        try:
            data= get_weather(city)
            weather = {
                "city": city,
                "temperature": round(data["main"]["temp"]-273.15),
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "visibility": data["visibility"]/1000,
            }
            logger.info(f"Temperature for the {city} successfully fetched {weather}")
        except KeyError as e:
            logger.error(f"Key Error: {e}")
            error = "Unable to find the key"
        except ConnectTimeout as e:
            logger.error(f"Connect Timeout Error: {e}")
            error = "Connection timeout when reaching to the API"
        except HTTPError as e:
            logger.error(f"HTTP Error: {e}")
            error = "Unable to connect to the API"
        except Exception as e:
            logger.error(f"An unknown Error: {e}")
            error = "Unknown error"
    else:
        logger.error("No city provided!")
        error = "No city provided!"
    return render_template("index.html",city=city,weather = weather,error=error)

#Returns json data for the city
def get_weather(city):
    response = requests.get(f"{BASE_URL}?q={city}&appid={API_KEY}")
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    app.run(debug=True)
```

### 4. Create the HTML Template
Inside a `templates/` folder, create an `index.html` file:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Weather App</title>
</head>
<body>
    <h1>Weather Dashboard</h1>
    <form method="post">
        <input type="text" name="city" placeholder="Enter city" required>
        <button type="submit">Get Weather</button>
    </form>
    {% if weather %}
        <h2>{{ weather.city }}</h2>
        <p>Temperature: {{ weather.temperature }}°C</p>
        <p>Description: {{ weather.description }}</p>
    {% endif %}
    {% if error %}
        <p style="color: red;">{{ error }}</p>
    {% endif %}
</body>
</html>
```

### 5. Deploy on AWS EC2
1. **Launch an EC2 instance** (Ubuntu/Windows)
2. **SSH into the instance:**
   ```sh
   ssh -i your-key.pem ec2-user@your-ec2-public-ip
   ```
3. **Install Python & Flask:**
   ```sh
   sudo apt update && sudo apt install python3-pip -y
   pip3 install flask requests
   ```
4. **Transfer project files using SCP or Git.**
5. **Run Flask in the background:**
   ```sh
   nohup python3 app.py --host=0.0.0.0 --port=5000 &
   ```

### 6. Access the Application
Visit: `http://your-ec2-public-ip:5000/`

## Future Enhancements
- Use **Gunicorn & Nginx** for better performance
- Implement **Docker** for containerization
- Add **error handling and logging**
- Integrate **geolocation-based weather fetching**

## License
This project is open-source and free to use.

## Run this application on Docker

Use the below command to build the image:
```
docker build -t weather-app:v1 . --no-cache
```
Once the image is build to run the image use 
Use the below command to build the image:
```
docker run -itd -p 5000:5000 weather-app:v1
```

---

Feel free to contribute or provide feedback! 😊

