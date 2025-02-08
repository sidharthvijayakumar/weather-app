from flask import Flask, request, render_template
import requests

app = Flask(__name__)

API_KEY = "dab002b477257dd1881d9f8b5bd5fefc" # Replace with actual API Key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"  

@app.route("/")
def home():
    city = request.args.get("city", "Pune")
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()
    
    if response.get("main"):
        weather = {
            "city": response["name"],
            "temperature": response["main"]["temp"],
            "description": response["weather"][0]["description"]
        }
        return render_template("index.html", weather=weather)
    else:
        return "<h3>City not found. Please try again.</h3>"
def get_weather(city):
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    return response.json()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
