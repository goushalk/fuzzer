from flask import Flask, render_template, request, jsonify
import json
import subprocess
import os

app = Flask(__name__)

@app.route('/xss', methods=['GET'])
def xss_form():
    # Render the form for user input
    return render_template('index.html')

@app.route('/xss', methods=['POST'])
def process_xss():
    url = request.json.get('url')
    if url:
        # Sanitize the URL for safety
        if os.path.exists('xxs.json'):
            os.remove('xss.json')  
        # Run the wfuzz command and capture the output using subprocess
        try:
            os.system(f"wfuzz -c -z file,xss.txt -f xss.json,json -u {url}?q=FUZZ")
        except:
            return "Error "
    return jsonify({"error": "Invalid request"}), 400

if __name__ == '__main__':
    app.run(debug=True)
