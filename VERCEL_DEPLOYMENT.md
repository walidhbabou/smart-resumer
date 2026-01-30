# Railway Deployment Instructions

## Deploy Backend to Railway

1. **Go to Railway.app and sign up/login**
   - Visit: https://railway.app

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Authorize Railway to access your GitHub
   - Select your repository: `walidhbabou/smart-resumer`

3. **Configure Backend Service**
   - Railway will auto-detect the Dockerfile
   - Set **Root Directory**: `backend`
   
4. **Add Environment Variables**
   Go to Variables tab and add:
   ```
   AI_PROVIDER=mock
   ENVIRONMENT=production
   DEBUG=False
   PORT=8000
   CORS_ORIGINS=https://your-vercel-app.vercel.app
   ```

5. **Deploy**
   - Railway will automatically build and deploy
   - You'll get a URL like: `https://your-app.railway.app`

6. **Update Vercel Frontend**
   - Go to Vercel Dashboard → Your Project → Settings → Environment Variables
   - Add:
     ```
     VITE_API_URL = https://your-app.railway.app
     ```
   - Redeploy the frontend

## Alternative: Deploy Backend to Render

1. **Go to Render.com and sign up/login**
   - Visit: https://render.com

2. **Create New Web Service**
   - Connect GitHub repo: `walidhbabou/smart-resumer`
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Environment Variables**
   ```
   PYTHON_VERSION=3.11.0
   AI_PROVIDER=mock
   ENVIRONMENT=production
   DEBUG=False
   CORS_ORIGINS=https://your-vercel-app.vercel.app
   ```

4. **Deploy and get URL**
   - Copy the Render URL
   - Add to Vercel as `VITE_API_URL`

## Update CORS on Backend

Make sure backend allows your Vercel domain in CORS settings.
