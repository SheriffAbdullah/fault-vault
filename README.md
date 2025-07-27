# FaultVault

**Tell me your problems** - A simple, secure problem tracking application

## Overview

FaultVault is a minimalist web application for tracking and managing problems. Built with Flask, it features a clean interface, markdown support, and password-protected access.

## Features

- 🔐 **Password Protection** - Simple authentication system
- 📝 **Markdown Support** - Rich text formatting for problem descriptions
- 📱 **Responsive Design** - Works on desktop and mobile devices
- ✅ **CRUD Operations** - Create, Read, Update, Delete problems
- 🔍 **View Mode** - Full problem details with formatted markdown
- ⚠️ **Delete Confirmation** - Prevents accidental deletions
- 💾 **JSON Storage** - Simple file-based data persistence

## Tech Stack

- **Backend**: Python Flask
- **Frontend**: Bootstrap 5, Vanilla JavaScript
- **Storage**: JSON file
- **Deployment**: Vercel-ready

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fault-vault
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file:
   ```
   PASSWORD=hooman@FaultVault
   SECRET_KEY=your-super-secret-key-here
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the application**
   Open http://127.0.0.1:5000 in your browser

## Usage

1. **Login**: Use the password `hooman@FaultVault`
2. **Add Problems**: Click "Add Problem" button
3. **Edit Problems**: Click "Edit" on any problem card
4. **View Problems**: Click "View" to see full details with markdown rendering
5. **Delete Problems**: Click "Delete" and confirm in the popup

## Deployment

### Vercel Deployment

1. Push your code to GitHub
2. Connect your repository to Vercel
3. Set environment variables in Vercel dashboard:
   - `PASSWORD`: Your chosen password
   - `SECRET_KEY`: A secure random string
4. Deploy!

## File Structure

```
fault-vault/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── vercel.json           # Vercel deployment config
├── .env                  # Environment variables (local)
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── login.html       # Login page
│   └── main.html        # Main application
├── static/              # Static assets
│   └── css/
│       └── custom.css   # Custom styles
└── data/               # Data storage
    └── problems.json   # Problems data file
```

## API Endpoints

- `GET /` - Login page or redirect to app
- `POST /login` - Authentication
- `GET /app` - Main application page
- `GET /api/problems` - Get all problems
- `POST /api/problems` - Create new problem
- `GET /api/problems/<id>` - Get specific problem
- `PUT /api/problems/<id>` - Update problem
- `DELETE /api/problems/<id>` - Delete problem

## Security Features

- Session-based authentication
- CSRF protection via Flask's session management
- Password-protected access to all features
- Environment variable configuration

## License

MIT License - see LICENSE file for details

