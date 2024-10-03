from flask import *
import requests
from bs4 import BeautifulSoup
import threading
from urllib.parse import urljoin

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')
# Sample payloads for fuzzing
payloads = {
    "sql_injection": ["' OR '1'='1'", "' UNION SELECT NULL--", "' DROP TABLE users;--"],
    "xss": ['<script>alert(1)</script>', '<img src=x onerror=alert(1)>'],
    "buffer_overflow": ['A' * 5000]
}

# Function to send GET or POST requests
def send_request(url, method="GET", data=None, headers=None, cookies=None):
    if method == "GET":
        response = requests.get(url, headers=headers, cookies=cookies)
    elif method == "POST":
        response = requests.post(url, data=data, headers=headers, cookies=cookies)
    return response

# Function to add schema if missing and clean up the URL
def add_schema_if_missing(url):
    url = url.strip()  # Remove any leading/trailing spaces
    if not url.startswith(('http://', 'https://')):
        return 'http://' + url
    return url

# Function to extract all forms from a web page
def extract_forms(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    forms = soup.find_all('form')
    return forms

# Function to fuzz form fields
def fuzz_form(base_url, form, payloads):
    form_data = {}
    # Extract input fields and fill them with fuzzing payloads
    for input_field in form.find_all('input'):
        field_name = input_field.get('name')
        if field_name:
            form_data[field_name] = payloads['sql_injection'][0]  # Fuzzing with SQL injection payload for demo

    # Resolve the form action (relative or absolute)
    action = form.get('action')
    if not action:
        action = base_url  # Default to the base URL if no action is specified
    else:
        action = urljoin(base_url, action)  # Handle relative URLs by joining with base URL

    method = form.get('method').upper() if form.get('method') else 'POST'
    response = send_request(action, method=method, data=form_data)
    
    return response

# Function to check vulnerabilities in the response
def check_vulnerabilities(response):
    vulnerabilities = []
    if "SQL" in response.text or "database" in response.text:
        vulnerabilities.append("SQL Injection vulnerability found!")
    if "<script>" in response.text:
        vulnerabilities.append("XSS vulnerability found!")
    return vulnerabilities

# Function to fuzz headers and cookies
def fuzz_headers_and_cookies(url, payloads):
    headers = {
        'User-Agent': payloads['xss'][0],  # Fuzzing with XSS payload for User-Agent header
        'Referer': payloads['sql_injection'][0]  # Fuzzing with SQL injection payload for Referer header
    }
    cookies = {'session_id': payloads['sql_injection'][0]}  # Fuzzing with SQL injection payload for cookies

    response = send_request(url, headers=headers, cookies=cookies)
    return check_vulnerabilities(response)

# Function to fuzz URLs
def fuzz_url_params(url, payloads):
    vulnerabilities = []
    for payload in payloads['sql_injection']:
        fuzzed_url = f"{url}?id={payload}"
        response = send_request(fuzzed_url)
        vulnerabilities.extend(check_vulnerabilities(response))
    return vulnerabilities

# Function to fuzz forms concurrently
def fuzz_concurrently(url, forms, payloads):
    threads = []
    results = []

    def thread_func(form):
        response = fuzz_form(url, form, payloads)
        results.extend(check_vulnerabilities(response))

    for form in forms:
        thread = threading.Thread(target=thread_func, args=(form,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return results

@app.route('/fuzz', methods=['POST'])
def fuzz():
    target_url = request.json.get('url')
    if not target_url:
        return jsonify({"error": "No URL provided"}), 400

    target_url = add_schema_if_missing(target_url)

    vulnerabilities = {}

    # Fuzz URL parameters
    vulnerabilities['url_params'] = fuzz_url_params(target_url, payloads)

    # Fuzz headers and cookies
    vulnerabilities['headers_and_cookies'] = fuzz_headers_and_cookies(target_url, payloads)

    # Fuzz forms on the page
    response = send_request(target_url)
    forms = extract_forms(response.text)
    if forms:
        vulnerabilities['forms'] = fuzz_concurrently(target_url, forms, payloads)
    else:
        vulnerabilities['forms'] = ["No forms found on the page."]

    return jsonify(vulnerabilities)

if __name__ == "__main__":
    app.run(debug=True)
