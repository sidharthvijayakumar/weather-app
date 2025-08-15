from flask import Flask, request, render_template
import requests
import logging

logging.basicConfig(level=logging.DEBUG,format="%(asctime)s %(levelname)s %(funcName)s %(message)s")
logger=logging.getLogger(__name__)

app = Flask(__name__)

API_KEY = ""  # Replace with actual API Key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"



@app.route("/")
def home_page():
    city = request.args.get("city", "kochi")
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    try:
        response = get_weather(city)
        if response["main"]:
            weather = {
                "city": response["name"],
                "temperature": response["main"]["temp"],
                "description": response["weather"][0]["description"]
            }
            logger.info(weather)
            return render_template("index.html", weather=weather)
        else:
            return "<h3>City not found. Please try again.</h3>"
    except requests.exceptions.RequestException as e:
        logger.error(e)
        return "Unable to fetch weather."
    except KeyError as e:
        print(f"Key error occurred:{e} does not exist!")
        return "Unable to fetch weather.Due to key error, please try again later."


def get_weather(city):
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)