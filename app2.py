from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
@app.route('/')
def home():
    render_template('test.html')

@app.route('/xss', methods=['GET'])
def xss_form():
    # Render the form for user input
    return render_template('index.html')

@app.route('/xss', methods=['POST'])
def process_xss():
    url = request.form.get('url')
    if url:
        # Sanitize the URL for safety
        if os.path.exists('xss.json'):
            os.remove('xss.json')  # Corrected the file name here
        
        # Run the wfuzz command and capture the output using subprocess
        try:
            command = f"wfuzz -c -z file,wordlist/xss.txt -f xss.json,json -u {url}?q=FUZZ"
            os.system(command)
        except:
            return "Error while exec command."
    return render_template('xss.html')
            # subprocess.run(command, shell=True, check=True)
            # return jsonify({"status": "wfuzz executed successfully"}), 200
        # except subprocess.CalledProcessError as e:
        #     return jsonify({"error": f"Error executing wfuzz: {e}"}), 500
    # return jsonify({"error": "Invalid request"}), 400

@app.route('/xssview', methods=['GET'])
def xss_view():
    try:
        # Load the JSON data from the file you uploaded
        json_file_path = os.path.join(os.getcwd(), 'xss.json')
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        
        # Pass 'data' to the HTML template
        return render_template('json.html', data=data)
    
    except Exception as e:
        return f"Error loading JSON file: {e}"

@app.route('/zero_re', methods=['POST'])
def process_zero_re():
    url = request.json.get('url')
    if url:
        # Sanitize the URL for safety
        if os.path.exists('ze_redict.json'):
            os.remove('ze_redict.json')  # Corrected file name consistency
        
        # Run the wfuzz command and capture the output using subprocess
        try:
            command = f"wfuzz -c -z file,wordlist/zero_re.txt -f ze_redict.json,json -u {url}?redirect=FUZZ --hc 302"
            os.system(command)
        except:
            return "Error while exec command."
    #         subprocess.run(command, shell=True, check=True)
    #         return jsonify({"status": "wfuzz executed successfully"}), 200
    #     except subprocess.CalledProcessError as e:
    #         return jsonify({"error": f"Error executing wfuzz: {e}"}), 500
    # return jsonify({"error": "Invalid request"}), 400

@app.route('/sqli', methods=['POST'])
def process_sqli():
    url = request.json.get('url')
    if url:
        # Sanitize the URL for safety
        if os.path.exists('sqli.json'):
            os.remove('sqli.json')  
        
        # Run the wfuzz command and capture the output using subprocess
        try:
            command = f'wfuzz -c -z file,wordlist/sqli.txt --hc 404 -d "username=FUZZ&password=test" {url}'
            os.system(command)
        except:
            return "Error while exec command."
    #         subprocess.run(command, shell=True, check=True)
    #         return jsonify({"status": "wfuzz executed successfully"}), 200
    #     except subprocess.CalledProcessError as e:
    #         return jsonify({"error": f"Error executing wfuzz: {e}"}), 500
    # return jsonify({"error": "Invalid request"}), 400

if __name__ == '__main__':
    app.run(debug=True)
