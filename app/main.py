
import os
import json
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/contract-info')
def contract_info():
    try:
        with open('app/contract_info.json', 'r') as f:
            info = json.load(f)
        return jsonify(info)
    except FileNotFoundError:
        return jsonify({"error": "Contract not deployed yet. Run `python scripts/deploy.py`"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)
