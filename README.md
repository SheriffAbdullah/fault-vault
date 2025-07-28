# FaultVault

A minimal Flask application for problem tracking with PostgreSQL storage.

## Tech Stack

- **Backend**: Flask
- **Database**: PostgreSQL (Supabase)
- **Frontend**: Bootstrap 5, vanilla JavaScript
- **Deployment**: Vercel

## Features

- Password-protected authentication
- CRUD operations for problems
- Markdown support for descriptions
- Responsive UI
- Session management

## Local Development

### Prerequisites
- Python 3.7+
- PostgreSQL database (Supabase recommended)

### Setup
1. Clone repository:
   ```bash
   git clone <repository-url>
   cd fault-vault
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your values
   ```

4. Run application:
   ```bash
   python app.py
   ```

## Environment Variables

```
PASSWORD=your-app-password
SECRET_KEY=your-flask-secret-key
DATABASE_URL=postgresql://user:pass@host:port/db
```

## Database Schema

```sql
CREATE TABLE problems (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Deployment

### Vercel
1. Push code to GitHub
2. Connect repository to Vercel
3. Set environment variables in Vercel dashboard
4. Deploy

**Note**: Use Supabase Session Pooler URL for Vercel compatibility:
```
postgresql://postgres.project:password@aws-region.pooler.supabase.com:5432/postgres
```

## Project Structure

```
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── vercel.json        # Vercel configuration
├── templates/         # HTML templates
├── static/           # CSS and assets
└── .env              # Environment variables (local)
```

## License

MIT
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

GNU GPL License - see LICENSE file for details

