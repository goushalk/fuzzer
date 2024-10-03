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
            os.system(f"wfuzz -c -z file,wordlist/xss.txt -f xss.json,json -u {url}?q=FUZZ")
        except:
            return "Error "
    return jsonify({"error": "Invalid request"}), 400

@app.route('/zero_re', methods=['POST'])
def process_zero_re():
    url = request.json.get('url')
    if url:
        # Sanitize the URL for safety
        if os.path.exists('ze_redict.json'):
            os.remove('ze_redict.json')  
        # Run the wfuzz command and capture the output using subprocess
        try:
            os.system(f"wfuzz -c -z file,wordlist/zero_re.txt -f ze_redict.json,json -u {target}?redirect=FUZZ --hc 302" )
        except:
            return "Error "
    return jsonify({"error": "Invalid request"}), 400

@app.route('/sqli', methods=['POST'])
def process_sqli():
    url = request.json.get('url')
    if url:
        # Sanitize the URL for safety
        if os.path.exists('sqli.json'):
            os.remove('sqli.json')  
        # Run the wfuzz command and capture the output using subprocess
        try:
            os.system(f'wfuzz -c -z file,wordlist/sqli.txt --hc 404 -d "username=FUZZ&password=test" {url}')
        except:
            return "Error "
    return jsonify({"error": "Invalid request"}), 400

if __name__ == '__main__':
    app.run(debug=True)

