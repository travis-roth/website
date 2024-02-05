from flask import Flask, render_template, request, abort
import subprocess
from weather import get_current_weather
from waitress import serve

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/weather_home')
def weather_home():
    return render_template('/weather_proj/weather_home.html')

@app.route('/weather')
def get_weather():
    city = request.args.get('city')
    
    weather_data = get_current_weather(city)

    #city is not found by api
    if not weather_data['cod'] == 200:
        return render_template('/weather_proj/city-not-found.html')

    return render_template(
        "/weather_proj/weather.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}"
    )

@app.route('/resume')
def resume():
    return render_template('/resume.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('X-GitHub-Event') == 'push':
        try:
            # Execute a git pull command
            subprocess.run(['git', 'pull'], cwd='/home/ubuntu/website', check=True)
            return 'Pull successful', 200
        except subprocess.CalledProcessError as e:
            return f'Error during pull: {e}', 500
    else:
        abort(400)

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port = 8000)