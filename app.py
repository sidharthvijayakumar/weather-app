from flask import Flask, render_template, request,jsonify
import requests
import logging
from requests.exceptions import ConnectTimeout, HTTPError

# Logger setup
logging.basicConfig(level=logging.INFO,format="%(asctime)s;%(levelname)s;%(funcName)s;%(message)s")
logger = logging.getLogger(__name__)

# Config
API_KEY = "2e25eb832f01483d950b9b7b764adee4"
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

@app.route("/health",methods=["GET"])
def health():
    return jsonify(status="Healthy")
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80,debug=True)