from flask import Flask, render_template, request, send_file
import os
import pandas as pd

app = Flask(__name__)

def hid_dict(url, wordlist='wordlist/hid_dict.txt', output_file='hid_dict.csv'):
    if os.path.exists(output_file):
        os.remove(output_file)
    
    command = f"wfuzz -c -w {wordlist} -f {output_file},csv -u {url}/FUZZ/ --hc 404"
    os.system(command)

def subdomain_enum(url, wordlist='wordlist/subdomains.txt', output_file='subenum.csv'):
    if os.path.exists(output_file):
        os.remove(output_file)
    
    command = f"wfuzz -c -w {wordlist} -f {output_file},csv -u http://FUZZ.{url} --hc 404"
    os.system(command)

def wfuzz_xss_attack(url, wordlist='wordlist/xss.txt', output_file='xss_output.csv'):
    if os.path.exists(output_file):
        os.remove(output_file)
    
    command = f"wfuzz -c -z file,{wordlist} -f {output_file},csv -u {url}?q=FUZZ"
    os.system(command)

def wfuzz_zero_redirect_attack(url, wordlist='wordlist/zero_re.txt', output_file='ze_redict_output.csv'):
    if os.path.exists(output_file):
        os.remove(output_file)
    
    command = f"wfuzz -c -z file,{wordlist} -f {output_file},csv -u {url}?redirect=FUZZ --hc 302"
    os.system(command)

def wfuzz_sqli_attack(url, wordlist='wordlist/sqli.txt', output_file='sqli_output.csv'):
    if os.path.exists(output_file):
        os.remove(output_file)
    
    command = f"wfuzz -c -z file,{wordlist} --hc 404 -d 'username=FUZZ&password=test' -f {output_file},csv {url}"
    os.system(command)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        attack_type = request.form.get('attack_type')

        # Define the output file based on the attack type
        output_file = None
        if attack_type == 'xss':
            output_file = 'xss_output.csv'
            metigation='''To mitigate XSS, use input validation and output encoding to prevent untrusted scripts from being executed. Also, enable Content Security Policy (CSP) and sanitize any user-generated content.'''
            wfuzz_xss_attack(url, output_file=output_file)
        elif attack_type == 'zero_redirect':
            output_file = 'ze_redict_output.csv'
            metigation='''To mitigate open redirects, validate and whitelist all URLs, ensuring only trusted destinations are allowed. Avoid passing user-controlled input directly into redirects and use relative paths where possible.''' 
            wfuzz_zero_redirect_attack(url, output_file=output_file)
        elif attack_type == 'sqli':
            output_file = 'sqli_output.csv'
            metigation='''To mitigate SQL injection, use parameterized queries or prepared statements to prevent direct user input in SQL queries. Additionally, validate and sanitize inputs, and consider using stored procedures for executing SQL code safely.'''
            wfuzz_sqli_attack(url, output_file=output_file)
        elif attack_type == 'hid_dict':
            output_file = 'hid_dict.csv'
            metigation='''To mitigate hidden directory enumeration, use proper file permissions to restrict access, disable directory listing in web server configurations, and implement a robots.txt file to block web crawlers from accessing sensitive directories.'''
            hid_dict(url, output_file=output_file)
        elif attack_type == 'subdomain_enum':
            output_file = 'subenum.csv'
            metigation='''To mitigate subdomain enumeration, limit exposure by minimizing the number of subdomains, use DNS security configurations, and restrict public DNS records. Implement rate-limiting and CAPTCHAs to deter automated tools.'''
            subdomain_enum(url, output_file=output_file)
        
        # Read the CSV file to display its contents if it exists
        if output_file and os.path.exists(output_file):
            csv_data = pd.read_csv(output_file)
            csv_content = csv_data.to_html(index=False)  # Convert DataFrame to HTML table
        else:
            csv_content = "No results found or file does not exist."

        # Render the result page with CSV content and download link
        return render_template('result.html', url=url, attack_type=attack_type, csv_content=csv_content, output_file=output_file,metigation=metigation)

    return render_template('verytest.html')

@app.route('/landing_page')
def landing_page():
    return render_template('index.html')

@app.route('/download/<filename>')
def download_file(filename):
    """Route to download the CSV file."""
    file_path = os.path.join(os.getcwd(), filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return f"File {filename} not found.", 404

if __name__ == '__main__':
    app.run(debug=True)
