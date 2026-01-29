# Troubleshooting Guide

Common issues and solutions for SmartResume Analyzer.

---

## Table of Contents
- [Installation Issues](#installation-issues)
- [Backend Issues](#backend-issues)
- [Frontend Issues](#frontend-issues)
- [Docker Issues](#docker-issues)
- [API Connection Issues](#api-connection-issues)
- [AI Provider Issues](#ai-provider-issues)
- [File Upload Issues](#file-upload-issues)

---

## Installation Issues

### Python Version Error
```
ERROR: This package requires Python >=3.11
```

**Solution:**
```bash
# Check Python version
python --version

# Install Python 3.11+ from python.org
# Windows: Use installer from python.org
# Mac: brew install python@3.11
# Linux: sudo apt install python3.11
```

### Node.js Version Error
```
ERROR: The engine "node" is incompatible with this module
```

**Solution:**
```bash
# Check Node version
node --version

# Install Node 20+
# Windows: Download from nodejs.org
# Mac: brew install node@20
# Linux: nvm install 20
```

### pip install fails
```
ERROR: Could not find a version that satisfies the requirement
```

**Solution:**
```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install with verbose output
pip install -r requirements.txt -v

# Try without cache
pip install --no-cache-dir -r requirements.txt
```

---

## Backend Issues

### ModuleNotFoundError
```
ModuleNotFoundError: No module named 'app'
```

**Solution:**
```bash
# Ensure you're in the backend directory
cd backend

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run from backend directory
uvicorn app.main:app --reload
```

### Port 8000 Already in Use
```
ERROR: Address already in use
```

**Solution:**
```bash
# Windows - Find and kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn app.main:app --port 8001 --reload
```

### ImportError: pydantic_settings
```
ImportError: cannot import name 'BaseSettings' from 'pydantic'
```

**Solution:**
```bash
# Install pydantic-settings
pip install pydantic-settings

# Or reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

### CORS Error in Browser Console
```
Access to XMLHttpRequest has been blocked by CORS policy
```

**Solution:**
Edit `backend/app/core/config.py`:
```python
CORS_ORIGINS: List[str] = Field(
    default=["http://localhost:5173", "http://localhost:3000"],
    env="CORS_ORIGINS"
)
```

Or in `.env`:
```bash
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

---

## Frontend Issues

### npm install fails
```
npm ERR! code ERESOLVE
```

**Solution:**
```bash
# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Install with legacy peer deps
npm install --legacy-peer-deps
```

### Vite build error
```
ERROR: Cannot find module '@vitejs/plugin-react'
```

**Solution:**
```bash
# Reinstall dev dependencies
npm install --save-dev @vitejs/plugin-react

# Or full reinstall
rm -rf node_modules package-lock.json
npm install
```

### Port 5173 Already in Use
```
Port 5173 is in use, trying another one...
```

**Solution:**
```bash
# Kill process on port 5173
# Windows:
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:5173 | xargs kill -9

# Or specify different port in vite.config.ts
```

### TypeScript errors
```
Property 'xyz' does not exist on type...
```

**Solution:**
```bash
# Restart TypeScript server in VS Code
# Ctrl+Shift+P → "TypeScript: Restart TS Server"

# Check tsconfig.json settings
# Ensure all types are installed
npm install --save-dev @types/react @types/react-dom
```

### Tailwind styles not working
```
Styles not applying in browser
```

**Solution:**
1. Check `tailwind.config.js` content paths:
```javascript
content: [
  "./index.html",
  "./src/**/*.{js,ts,jsx,tsx}",
],
```

2. Verify `index.css` imports:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

3. Rebuild:
```bash
npm run build
```

---

## Docker Issues

### Docker daemon not running
```
Cannot connect to the Docker daemon
```

**Solution:**
- **Windows:** Start Docker Desktop
- **Mac:** Start Docker Desktop from Applications
- **Linux:** `sudo systemctl start docker`

### docker-compose command not found
```
docker-compose: command not found
```

**Solution:**
```bash
# Try docker compose (no hyphen) - newer Docker versions
docker compose up

# Or install docker-compose
# Windows/Mac: Included in Docker Desktop
# Linux:
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Build fails with network error
```
ERROR: failed to solve: failed to fetch
```

**Solution:**
```bash
# Check internet connection
# Try with --no-cache
docker-compose build --no-cache

# Or build individually
docker build -t backend ./backend
docker build -t frontend ./frontend
```

### Container keeps restarting
```
Container smartresume-backend is unhealthy
```

**Solution:**
```bash
# View logs
docker-compose logs backend
docker-compose logs frontend

# Check health endpoint
curl http://localhost:8000/health

# Rebuild without cache
docker-compose down
docker-compose up --build --force-recreate
```

### Permission denied errors (Linux)
```
Permission denied while trying to connect to Docker daemon
```

**Solution:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Log out and back in, or run:
newgrp docker
```

---

## API Connection Issues

### Network Error / ERR_CONNECTION_REFUSED
```
Error: Network Error
```

**Solution:**
1. **Check backend is running:**
   ```bash
   curl http://localhost:8000/health
   ```

2. **Check frontend API URL:**
   Edit `frontend/.env`:
   ```bash
   VITE_API_URL=http://localhost:8000
   ```

3. **Check firewall/antivirus:**
   - Allow ports 8000, 3000, 5173

4. **Try different browser:**
   - Clear cache and cookies
   - Disable extensions

### CORS Error
```
CORS policy: No 'Access-Control-Allow-Origin' header
```

**Solution:**
Update `backend/.env`:
```bash
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

Restart backend:
```bash
docker-compose restart backend
```

### Timeout Error
```
Error: timeout of 60000ms exceeded
```

**Solution:**
1. **AI processing takes time** - This is normal for real AI
2. **Increase timeout** in `frontend/src/services/api.ts`:
   ```typescript
   timeout: 120000, // 2 minutes
   ```
3. **Use mock provider** for testing:
   ```bash
   AI_PROVIDER=mock
   ```

---

## AI Provider Issues

### OpenAI API Error: Invalid API Key
```
Error: Incorrect API key provided
```

**Solution:**
1. **Check API key** in `backend/.env`:
   ```bash
   AI_API_KEY=sk-proj-...
   ```
2. **Verify on OpenAI website:** platform.openai.com
3. **Check key has permissions**
4. **No extra spaces** in .env file

### OpenAI Rate Limit Error
```
Error: Rate limit reached
```

**Solution:**
1. **Wait and retry**
2. **Upgrade OpenAI plan**
3. **Use mock provider:**
   ```bash
   AI_PROVIDER=mock
   ```

### Anthropic API Error
```
Error: authentication_error
```

**Solution:**
1. **Check API key** format: starts with `sk-ant-`
2. **Verify on Anthropic Console:** console.anthropic.com
3. **Check model name:**
   ```bash
   AI_MODEL=claude-3-5-sonnet-20241022
   ```

### Mock Provider Not Working
```
Analysis returns unrealistic data
```

**This is expected!** Mock provider generates dummy data for testing without API costs.

To use real AI:
```bash
# backend/.env
AI_PROVIDER=openai  # or anthropic
AI_API_KEY=your-real-key
```

---

## File Upload Issues

### File Upload Fails
```
Error: Only PDF files are supported
```

**Solution:**
- Ensure file has `.pdf` extension
- File must be actual PDF (not renamed Word doc)
- Check file size < 10MB

### PDF Text Extraction Fails
```
Error: No text could be extracted from the PDF
```

**Solution:**
1. **Scanned/Image PDFs** - Contains no text, only images
   - Use OCR tools to convert first
   - Or create text-based PDF

2. **Encrypted PDFs** - Password protected
   - Remove password protection
   - Use unencrypted version

3. **Corrupted PDF**
   - Try opening in PDF reader
   - Re-export from source document

### File Too Large
```
Error: File size exceeds maximum limit of 10MB
```

**Solution:**
1. **Compress PDF:**
   - Use Adobe Acrobat / online tools
   - Reduce image quality

2. **Increase limit** in `backend/.env`:
   ```bash
   MAX_FILE_SIZE_MB=20
   ```

---

## Development Issues

### Hot Reload Not Working

**Backend:**
```bash
# Ensure --reload flag is used
uvicorn app.main:app --reload

# Check file changes are saved
# Restart manually if needed
```

**Frontend:**
```bash
# Ensure dev server is running
npm run dev

# Check vite.config.ts
# Clear .vite cache
rm -rf node_modules/.vite
```

### Environment Variables Not Loading

**Solution:**
1. **File must be named** `.env` (not `.env.txt`)
2. **Must be in correct directory:**
   - Backend: `backend/.env`
   - Frontend: `frontend/.env`
3. **No quotes** around values:
   ```bash
   # Correct:
   AI_PROVIDER=openai
   
   # Wrong:
   AI_PROVIDER="openai"
   ```
4. **Restart server** after .env changes

### Tests Failing

```bash
# Backend tests
cd backend
pytest -v

# If imports fail, add:
export PYTHONPATH="${PYTHONPATH}:${PWD}"
pytest -v

# Frontend tests
cd frontend
npm test
```

---

## Getting More Help

### Enable Debug Logging

**Backend** (`backend/.env`):
```bash
DEBUG=True
LOG_LEVEL=DEBUG
```

**View detailed logs:**
```bash
docker-compose logs -f backend
```

### Check Health Endpoints

```bash
# Backend health
curl http://localhost:8000/health

# Frontend health (when using Docker)
curl http://localhost:3000/health
```

### Common Log Messages

**Normal operation:**
```
INFO - Starting SmartResume Analyzer v1.0.0
INFO - Successfully analyzed CV with score: 85.5
```

**Configuration issues:**
```
WARNING - No API key provided, falling back to mock provider
ERROR - Failed to extract text from PDF
```

---

## Still Having Issues?

1. **Check documentation:**
   - README.md
   - QUICKSTART.md
   - ARCHITECTURE.md

2. **Review logs carefully:**
   ```bash
   docker-compose logs -f
   ```

3. **Try fresh install:**
   ```bash
   docker-compose down -v
   rm -rf backend/__pycache__ frontend/node_modules
   docker-compose up --build
   ```

4. **Search GitHub Issues** (if public repo)

5. **Ask for help** with:
   - Error message
   - OS and versions
   - Steps to reproduce
   - Log output

---

**Most issues are due to:**
- ❌ Missing dependencies
- ❌ Wrong directory
- ❌ Port conflicts
- ❌ Environment variables
- ❌ Docker not running

**Always check these first! ✅**
