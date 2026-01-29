# Quick Start Guide

Get SmartResume Analyzer running in 5 minutes! ⚡

---

## Method 1: Docker (Recommended) 🐳

**Prerequisites:** Docker Desktop installed

```bash
# 1. Navigate to project folder
cd "c:\Users\PC\Desktop\Nouveau dossier"

# 2. Copy environment file
copy .env.example .env

# 3. Start the application
docker-compose up --build
```

**Access the application:**
- 🌐 Frontend: http://localhost:3000
- 🔧 Backend API: http://localhost:8000
- 📚 API Docs: http://localhost:8000/api/docs

**Note:** By default, it uses **mock AI provider** (no API key needed for testing).

---

## Method 2: Local Development 💻

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment (Windows)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment
copy .env.example .env

# Run server
uvicorn app.main:app --reload
```

Backend runs at: http://localhost:8000

### Frontend Setup

Open a new terminal:

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Setup environment
copy .env.example .env

# Run development server
npm run dev
```

Frontend runs at: http://localhost:5173

---

## Using the Application 📝

1. **Open the frontend** in your browser
2. **Upload a CV** (PDF format)
3. **Paste a job description**
4. **Click "Analyze CV"**
5. **View results:** score, matching skills, missing skills, and recommendations

---

## Using Real AI (Optional) 🤖

To use OpenAI or Anthropic instead of mock AI:

### Edit `.env` file:

**For OpenAI:**
```bash
AI_PROVIDER=openai
AI_API_KEY=sk-your-openai-key-here
AI_MODEL=gpt-4
```

**For Anthropic:**
```bash
AI_PROVIDER=anthropic
AI_API_KEY=sk-ant-your-anthropic-key-here
AI_MODEL=claude-3-5-sonnet-20241022
```

Then restart the application.

---

## Troubleshooting 🔧

### Backend won't start
- Check Python version: `python --version` (need 3.11+)
- Check if port 8000 is in use
- Review backend logs

### Frontend won't start
- Check Node version: `node --version` (need 20+)
- Try `npm install` again
- Check if port 5173/3000 is in use

### Docker issues
- Ensure Docker Desktop is running
- Try `docker-compose down` then `docker-compose up --build`
- Check Docker logs: `docker-compose logs -f`

### API connection errors
- Verify backend is running
- Check CORS settings
- Ensure correct API URL in frontend `.env`

---

## Testing the API 🧪

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# Analyze CV (Windows PowerShell)
curl -X POST http://localhost:8000/api/analyze `
  -F "cv_file=@path/to/your/cv.pdf" `
  -F "job_description=Looking for a senior Python developer with FastAPI experience..."
```

### Using Swagger UI

Visit http://localhost:8000/api/docs and use the interactive interface.

---

## Next Steps 🎯

- Review the [README.md](README.md) for detailed documentation
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment
- Read [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

---

## Sample Job Description for Testing

```
We are looking for a Senior Full Stack Developer with:

Required Skills:
- Python and FastAPI
- React and TypeScript
- Docker and containerization
- REST API design
- Database design (SQL/NoSQL)
- Git version control

Nice to have:
- AWS or Azure experience
- CI/CD pipeline setup
- Microservices architecture
- React Query / Redux
- Tailwind CSS

Responsibilities:
- Design and implement scalable web applications
- Write clean, maintainable code
- Collaborate with cross-functional teams
- Participate in code reviews
- Mentor junior developers
```

---

## Resources 📚

- **FastAPI Docs:** https://fastapi.tiangolo.com/
- **React Docs:** https://react.dev/
- **OpenAI API:** https://platform.openai.com/docs
- **Anthropic API:** https://docs.anthropic.com/

---

**Happy Analyzing! 🚀**
