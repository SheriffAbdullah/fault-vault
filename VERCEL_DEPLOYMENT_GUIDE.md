# 🚀 Deploying FaultVault to Vercel

This guide will walk you through deploying your FaultVault Flask application to Vercel.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Account**: Your code should be in a GitHub repository
3. **Git**: Make sure Git is installed on your machine

## Step 1: Prepare Your Code for Deployment

Your project is already configured for Vercel! Here's what's already set up:

### ✅ Project Structure
```
fault-vault/
├── app.py                 # Main Flask application
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
├── templates/            # HTML templates
│   ├── base.html
│   ├── login.html
│   └── main.html
├── static/              # Static files (CSS)
│   └── css/
│       └── custom.css
├── data/                # Data storage
│   └── problems.json
└── .env                 # Environment variables (DO NOT COMMIT)
```

### ✅ Configuration Files

**vercel.json** - Already configured correctly:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "app.py"
    }
  ]
}
```

**requirements.txt** - All dependencies listed:
```
flask
python-dotenv
markdown
gunicorn
```

## Step 2: Push Your Code to GitHub

1. **Initialize Git repository** (if not already done):
   ```bash
   git init
   ```

2. **Add all files** (but exclude .env):
   ```bash
   # Create .gitignore if it doesn't exist
   echo ".env" > .gitignore
   echo "__pycache__/" >> .gitignore
   echo "*.pyc" >> .gitignore
   
   git add .
   git commit -m "Initial commit: FaultVault Flask app"
   ```

3. **Create GitHub repository**:
   - Go to [github.com](https://github.com) and create a new repository
   - Name it `fault-vault` (or any name you prefer)
   - **Don't** initialize with README, .gitignore, or license (since you already have files)

4. **Push to GitHub**:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/fault-vault.git
   git branch -M main
   git push -u origin main
   ```

## Step 3: Deploy to Vercel

### Option A: Deploy via Vercel Dashboard (Recommended)

1. **Login to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Sign in with your GitHub account

2. **Import Project**:
   - Click "New Project"
   - Select "Import Git Repository"
   - Choose your `fault-vault` repository
   - Click "Import"

3. **Configure Project**:
   - **Project Name**: `fault-vault` (or your preferred name)
   - **Framework Preset**: Leave as "Other" (Vercel will auto-detect Flask)
   - **Root Directory**: Leave as `./`
   - Click "Deploy"

### Option B: Deploy via Vercel CLI

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel
   ```
   
   Follow the prompts:
   - Link to existing project? **N**
   - What's your project's name? **fault-vault**
   - In which directory is your code located? **./**

## Step 4: Configure Environment Variables

1. **In Vercel Dashboard**:
   - Go to your project dashboard
   - Click on "Settings" tab
   - Click on "Environment Variables"

2. **Add Required Variables**:
   ```
   Variable Name: PASSWORD
   Value: hooman@FaultVault
   
   Variable Name: SECRET_KEY
   Value: your-super-secret-key-change-this-in-production
   ```

3. **Important**: Make sure to set these for **Production** environment

## Step 5: Handle Data Persistence

⚠️ **Important**: Vercel functions are stateless, so the JSON file storage won't persist between deployments.

### Recommended Solutions:

1. **Vercel KV (Redis)** - For simple key-value storage
2. **Supabase** - Free PostgreSQL database
3. **MongoDB Atlas** - Free MongoDB database
4. **Planetscale** - Free MySQL database

For now, your app will work but data will reset on each deployment. Let me know if you'd like help setting up a database!

## Step 6: Access Your App

1. **After deployment**, Vercel will provide URLs:
   - **Production**: `https://your-project-name.vercel.app`
   - **Preview**: `https://your-project-name-git-main-username.vercel.app`

2. **Test your app**:
   - Visit the URL
   - Login with password: `hooman@FaultVault`
   - Add/edit/delete problems

## Step 7: Custom Domain (Optional)

1. **In Vercel Dashboard**:
   - Go to "Settings" → "Domains"
   - Add your custom domain
   - Follow DNS configuration instructions

## Troubleshooting

### Common Issues:

1. **Build Failed**:
   - Check `requirements.txt` has all dependencies
   - Ensure `vercel.json` points to correct file

2. **Environment Variables Not Working**:
   - Make sure variables are set in Vercel dashboard
   - Redeploy after adding variables

3. **Static Files Not Loading**:
   - Ensure CSS files are in `static/` directory
   - Check file paths in templates

4. **Data Not Persisting**:
   - This is expected with JSON file storage
   - Consider upgrading to a database solution

## Next Steps

1. **Set up a database** for persistent storage
2. **Configure custom domain** if desired
3. **Set up monitoring** and analytics
4. **Add HTTPS security headers**

## Support

If you encounter any issues:
1. Check Vercel deployment logs
2. Ensure all environment variables are set
3. Verify GitHub repository has all necessary files

Your FaultVault app is now ready for deployment! 🎉
