from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import os
from datetime import datetime
import logging
from dotenv import load_dotenv
import markdown
import psycopg2
from psycopg2.extras import RealDictCursor

load_dotenv()

# --- Constants ---
PASSWORD = os.getenv("PASSWORD")
DATABASE_URL = os.getenv("DATABASE_URL")

# --- App Initialization ---
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "your-secret-key-here")

# --- Database Functions ---
def get_db_connection():
    """Get database connection with Vercel optimizations."""
    try:
        # Add connection timeout for Vercel
        conn = psycopg2.connect(
            DATABASE_URL, 
            cursor_factory=RealDictCursor,
            connect_timeout=10,
            keepalives=1,
            keepalives_idle=600,
            keepalives_interval=30,
            keepalives_count=3
        )
        return conn
    except Exception as e:
        logging.error(f"Database connection error: {e}")
        return None

def init_db():
    """Initialize the database with problems table."""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS problems (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    description TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            cur.close()
            conn.close()
            logging.info("Database initialized successfully")
        except Exception as e:
            logging.error(f"Database initialization error: {e}")
            if conn:
                conn.close()

def load_problems():
    """Load problems from database."""
    conn = get_db_connection()
    if not conn:
        return []
    
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM problems ORDER BY created_at DESC')
        problems = cur.fetchall()
        cur.close()
        conn.close()
        return [dict(problem) for problem in problems]
    except Exception as e:
        logging.error(f"Error loading problems: {e}")
        if conn:
            conn.close()
        return []

def save_problems(problems):
    """Legacy function - not used with database."""
    pass

def convert_markdown(text):
    """Convert markdown text to HTML."""
    return markdown.markdown(text)

# Initialize database on startup (only if needed)
try:
    init_db()
except Exception as e:
    logging.error(f"Database initialization failed: {e}")

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
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO problems (title, description) 
            VALUES (%s, %s) RETURNING id, created_at, last_modified
        ''', (title, description))
        
        result = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        
        new_problem = {
            "id": result['id'],
            "title": title,
            "description": description,
            "created_at": result['created_at'].isoformat(),
            "last_modified": result['last_modified'].isoformat()
        }
        
        logging.info(f"Adding new problem: {title}")
        return jsonify({'success': True, 'problem': new_problem})
    except Exception as e:
        logging.error(f"Error adding problem: {e}")
        if conn:
            conn.close()
        return jsonify({'error': 'Failed to save problem'}), 500

@app.route('/api/problems/<int:problem_id>', methods=['PUT'])
def edit_problem(problem_id):
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    
    if not title or not description:
        return jsonify({'error': 'Title and description are required'}), 400
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cur = conn.cursor()
        cur.execute('''
            UPDATE problems 
            SET title = %s, description = %s, last_modified = CURRENT_TIMESTAMP 
            WHERE id = %s
            RETURNING id, title, description, created_at, last_modified
        ''', (title, description, problem_id))
        
        result = cur.fetchone()
        if not result:
            conn.close()
            return jsonify({'error': 'Problem not found'}), 404
        
        conn.commit()
        cur.close()
        conn.close()
        
        updated_problem = {
            "id": result['id'],
            "title": result['title'],
            "description": result['description'],
            "created_at": result['created_at'].isoformat(),
            "last_modified": result['last_modified'].isoformat()
        }
        
        logging.info(f"Editing problem: {title}")
        return jsonify({'success': True, 'problem': updated_problem})
    except Exception as e:
        logging.error(f"Error updating problem: {e}")
        if conn:
            conn.close()
        return jsonify({'error': 'Failed to update problem'}), 500

@app.route('/api/problems/<int:problem_id>', methods=['DELETE'])
def delete_problem(problem_id):
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'Unauthorized'}), 401
    
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500
    
    try:
        cur = conn.cursor()
        cur.execute('DELETE FROM problems WHERE id = %s', (problem_id,))
        
        if cur.rowcount == 0:
            conn.close()
            return jsonify({'error': 'Problem not found'}), 404
        
        conn.commit()
        cur.close()
        conn.close()
        
        logging.info(f"Deleted problem with ID: {problem_id}")
        return jsonify({'success': True})
    except Exception as e:
        logging.error(f"Error deleting problem: {e}")
        if conn:
            conn.close()
        return jsonify({'error': 'Failed to delete problem'}), 500

@app.route('/api/problems/<int:problem_id>', methods=['GET'])
def get_problem(problem_id):
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'Unauthorized'}), 401
    
    problems = load_problems()
    problem = next((p for p in problems if p["id"] == problem_id), None)
    
    if not problem:
        return jsonify({'error': 'Problem not found'}), 404
    
    return jsonify(problem)

@app.route('/debug')
def debug():
    """Debug endpoint to check environment variables (remove in production)."""
    if 'authenticated' not in session or not session['authenticated']:
        return jsonify({'error': 'Unauthorized'}), 401
    
    return jsonify({
        'PASSWORD_SET': bool(PASSWORD),
        'DATABASE_URL_SET': bool(DATABASE_URL),
        'SECRET_KEY_SET': bool(app.secret_key and app.secret_key != 'your-secret-key-here'),
        'DATABASE_URL_PREFIX': DATABASE_URL[:30] + '...' if DATABASE_URL else None,
    })

# --- Run the app ---
if __name__ == '__main__':
    app.run(debug=True)
