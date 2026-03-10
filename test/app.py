from flask import Flask
from datetime import datetime

app = Flask(__name__)

time_now = datetime.now().strftime('%H:%M:%S')

@app.route('/')
def index():
    return f"<h1>{time_now}</h1>"

@app.route("/links")
def google():
    body =  """<a href="https://www.google.com", target="_blank">Google</a><br />
    <a href="https://www.bing.com", target="_blank">Bing</a>"""
    return body

if __name__ == "__main__":
    app.run(debug=True)