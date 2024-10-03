from flask import *
import requests
import os
app = Flask(__name__)

def add_schema_if_missing(url):
    url = url.strip()  # Remove any leading/trailing spaces
    if not url.startswith(('http://', 'https://')):
        return 'http://' + url
    return url

def send_request(url, method="GET", data=None, headers=None, cookies=None):
    if method == "GET":
        response = requests.get(url, headers=headers, cookies=cookies)
    elif method == "POST":
        response = requests.post(url, data=data, headers=headers, cookies=cookies)
    return response


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/xss')
def zero_redict():    
    target_url = request.json.get('url')
    if not target_url:
        return jsonify({"error": "No URL provided"}), 400

    target_url = add_schema_if_missing(target_url)
    os.system(target_url+"re")
if __name__ == "__main__":
    app.run(debug=True)