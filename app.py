from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import os
from datetime import datetime
import logging
from dotenv import load_dotenv
import markdown

load_dotenv()

# --- Constants ---
PASSWORD = os.getenv("PASSWORD")
DATA_FILE = "data/problems.json"

# --- App Initialization ---
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your-secret-key-here")  # Add to .env file

# --- Helper Functions ---
def load_problems():
    """Loads problems from the JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_problems(problems):
    """Saves problems to the JSON file."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(problems, f, indent=4)

def convert_markdown(text):
    """Convert markdown text to HTML."""
    return markdown.markdown(text)

# --- Routes ---
@app.route('/')
def index():
    if 'authenticated' in session and session['authenticated']:
        return redirect(url_for('main_app'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    password = request.form.get('password')
    if password == PASSWORD:
        session['authenticated'] = True
        logging.info("Successful login")
        return jsonify({'success': True, 'redirect': url_for('main_app')})
    else:
        logging.warning("Failed login attempt")
        return jsonify({'success': False, 'message': 'Incorrect password.'})

@app.route('/logout')
def logout():
    session.pop('authenticated', None)
    return redirect(url_for('index'))

@app.route('/app')
def main_app():
    if 'authenticated' not in session or not session['authenticated']:
        return redirect(url_for('index'))
    
    problems = load_problems()
    # Sort problems by newest first
    problems_sorted = sorted(problems, key=lambda x: x.get('created_at', x.get('timestamp', '')), reverse=True)
    
    return render_template('main.html', problems=problems_sorted)

@app.route('/api/problems', methods=['GET'])
def get_problems():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'Unauthorized'}), 401
    
    problems = load_problems()
    problems_sorted = sorted(problems, key=lambda x: x.get('created_at', x.get('timestamp', '')), reverse=True)
    return jsonify(problems_sorted)

@app.route('/api/problems', methods=['POST'])
def add_problem():
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    
    if not title or not description:
        return jsonify({'error': 'Title and description are required'}), 400
    
    problems = load_problems()
    new_problem = {
        "id": max([p.get('id', 0) for p in problems], default=0) + 1,
        "title": title,
        "description": description,
        "created_at": datetime.now().isoformat(),
        "last_modified": datetime.now().isoformat()
    }
    problems.append(new_problem)
    save_problems(problems)
    
    logging.info(f"Adding new problem: {title}")
    return jsonify({'success': True, 'problem': new_problem})

@app.route('/api/problems/<int:problem_id>', methods=['PUT'])
def edit_problem(problem_id):
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    
    if not title or not description:
        return jsonify({'error': 'Title and description are required'}), 400
    
    problems = load_problems()
    problem = next((p for p in problems if p["id"] == problem_id), None)
    
    if not problem:
        return jsonify({'error': 'Problem not found'}), 404
    
    problem["title"] = title
    problem["description"] = description
    problem["last_modified"] = datetime.now().isoformat()
    
    save_problems(problems)
    logging.info(f"Editing problem: {title}")
    return jsonify({'success': True, 'problem': problem})

@app.route('/api/problems/<int:problem_id>', methods=['DELETE'])
def delete_problem(problem_id):
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'Unauthorized'}), 401
    
    problems = load_problems()
    problem = next((p for p in problems if p["id"] == problem_id), None)
    
    if not problem:
        return jsonify({'error': 'Problem not found'}), 404
    
    problems = [p for p in problems if p["id"] != problem_id]
    save_problems(problems)
    
    logging.info(f"Deleted problem with ID: {problem_id}")
    return jsonify({'success': True})

@app.route('/api/problems/<int:problem_id>', methods=['GET'])
def get_problem(problem_id):
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'Unauthorized'}), 401
    
    problems = load_problems()
    problem = next((p for p in problems if p["id"] == problem_id), None)
    
    if not problem:
        return jsonify({'error': 'Problem not found'}), 404
    
    return jsonify(problem)

# --- Run the app ---
if __name__ == '__main__':
    app.run(debug=True)
