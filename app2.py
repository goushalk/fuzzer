from flask import Flask, render_template
import json
import os

app = Flask(__name__)

@app.route('/')
def json_view():
    try:
        # Load the JSON data from the file you uploaded
        json_file_path = os.path.join(os.getcwd(), 'output.json')
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        
        # Pass 'data' to the HTML template
        return render_template('data.html', data=data)
    
    except Exception as e:
        return f"Error loading JSON file: {e}"

if __name__ == '__main__':
    app.run(debug=True)
