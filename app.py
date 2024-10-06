from flask import *
import json
import os

app = Flask(__name__)

# from flask import Flask, request, render_template, redirect, url_for, jsonify



@app.route('/')
def home():
    return render_template('test.html')

@app.route('/fuzz', methods=['POST'])
def fuzz():
    url = request.form.get('url')  # Getting the URL from the form
    if url:
        # Perform fuzzing logic with the URL
        # For now, we will just print the URL and return it for testing
        print(f"Received URL for fuzzing: {url}")
        return jsonify({'success': True, 'message': f'Fuzzing started on: {url}'})
    else:
        return jsonify({'success': False, 'message': 'Invalid URL'}), 400



# XSS Vulnerability Testing
@app.route('/xss', methods=['POST'])
def xss():
    url = request.form.get('url')
    if url:
        # Sanitize the URL for safety
        if os.path.exists('xss.json'):
            os.remove('xss.json')
        try:
            os.system(f"wfuzz -c -z file,wordlist/xss.txt -f xss.json,json -u {url}?q=FUZZ")
        except:
            return "Error"
    return render_template('xss.html')


# Endpoint to display XSS test results
@app.route('/xss/results')
def xss_results():
    if os.path.exists('xss.json'):
        with open('xss.json') as f:
            data = json.load(f)
        return render_template('results.html', results=data)
    return "No results found for XSS testing."


# Zero Redirect Testing
@app.route('/zero_re', methods=['GET,POST'])
def zero_re():
    url = request.form.get('url')
    if url:
        # Sanitize the URL for safety
        if os.path.exists('ze_redict.json'):
            os.remove('ze_redict.json')
        try:
            os.system(f"wfuzz -c -z file,wordlist/zero_re.txt -f ze_redict.json,json -u {url}?redirect=FUZZ --hc 302")
        except:
            return "Error"
    return render_template('dir.html')


# Endpoint to display Zero Redirect test results
@app.route('/zero_re/results')
def zero_re_results():
    if os.path.exists('ze_redict.json'):
        with open('ze_redict.json') as f:
            data = json.load(f)
        return render_template('results.html', results=data)
    return "No results found for Zero Redirect testing."


# SQL Injection Testing
@app.route('/sqli', methods=['GET','POST'])
def sqli():
    url = request.form.get('url')
    if url:
        # Sanitize the URL for safety
        if os.path.exists('sqli.json'):
            os.remove('sqli.json')
        try:
            os.system(f'wfuzz -c -z file,wordlist/sqli.txt --hc 404 -d "username=FUZZ&password=test" {url}')
        except:
            return "Error"
    return render_template('sqli.html')


# Endpoint to display SQLi test results
@app.route('/sqli/results')
def sqli_results():
    if os.path.exists('sqli.json'):
        with open('sqli.json') as f:
            data = json.load(f)
        return render_template('results.html', results=data)
    return "No results found for SQL Injection testing."


# Directory Route
@app.route('/dir')
def dir():
    return render_template('dir.html')


if __name__ == "__main__":
    app.run(debug=True)
