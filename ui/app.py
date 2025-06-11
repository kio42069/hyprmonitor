from flask import Flask, render_template, request, send_from_directory, abort
import os
import json
from datetime import datetime

app = Flask(__name__)

USER = os.getlogin()
BASE_DIR = f"/home/{USER}/.config/hypr/hyprmonitor"

# Helper to load a json file
def load_json(filename):
    try:
        with open(os.path.join(BASE_DIR, filename), 'r') as f:
            return json.load(f)
    except Exception:
        return None

@app.route('/')
def index():
    all_data = load_json('all.json')
    apps_data = load_json('apps.json')
    return render_template('index.html', all_data=all_data, apps_data=apps_data)

@app.route('/date', methods=['GET'])
def date_view():
    date = request.args.get('date')
    if not date:
        return render_template('date.html', all_data=None, apps_data=None, date=None)
    all_data = load_json(f'all_{date}.json')
    apps_data = load_json(f'apps_{date}.json')
    return render_template('date.html', all_data=all_data, apps_data=apps_data, date=date)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').lower()
    all_data = load_json('all.json')
    apps_data = load_json('apps.json')
    results = {}
    if all_data:
        for k, v in all_data.items():
            if query in k.lower():
                results[k] = v
    if not results and apps_data:
        for k, v in apps_data.items():
            if query in k.lower():
                results[k] = v
    return render_template('search.html', query=query, results=results)

@app.route('/download/<filename>')
def download(filename):
    if not filename.endswith('.json'):
        abort(404)
    return send_from_directory(BASE_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
