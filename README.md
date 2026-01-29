# SmartResume Analyzer 🚀

**AI-powered CV analysis platform** that matches resumes with job descriptions and provides actionable insights for candidates and recruiters.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![React](https://img.shields.io/badge/react-18.2-blue.svg)
![FastAPI](https://img.shields.io/badge/fastapi-0.109-green.svg)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Development](#development)
- [Deployment](#deployment)
- [Configuration](#configuration)
- [Testing](#testing)
- [Contributing](#contributing)

---

## 🎯 Overview

SmartResume Analyzer is a demo full-stack application that demonstrates **clean architecture**, **clean code principles**, and **professional development practices**. It leverages AI (OpenAI GPT-4, Anthropic Claude, or mock mode) to analyze CVs against job descriptions and provide:

- **Match Score** (0-100%)
- **Matching Skills** - Skills present in both CV and job description
- **Missing Skills** - Important skills from job description not in CV
- **Strengths** - Candidate's key strengths
- **Areas for Improvement** - Actionable suggestions
- **Detailed Recommendations** - Comprehensive analysis

---

## ✨ Features

### Backend (FastAPI)
- ✅ RESTful API with OpenAPI/Swagger documentation
- ✅ PDF text extraction from uploaded CVs
- ✅ AI integration with abstraction layer (OpenAI, Anthropic, Mock)
- ✅ Pydantic schemas for data validation
- ✅ Clean architecture with separation of concerns
- ✅ Structured logging
- ✅ CORS configuration
- ✅ Docker support
- ✅ Environment-based configuration
- ✅ Health check endpoints

### Frontend (React)
- ✅ Modern React 18 with TypeScript
- ✅ Tailwind CSS for responsive design
- ✅ React Query for state management
- ✅ Drag & drop file upload
- ✅ Real-time form validation
- ✅ Loading and error states
- ✅ Toast notifications
- ✅ Clean component architecture
- ✅ Mobile-responsive UI
- ✅ Docker + Nginx deployment

---

## 🏗️ Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│                 │         │                  │         │                 │
│  React Frontend │────────▶│  FastAPI Backend │────────▶│   AI Service    │
│  (TypeScript)   │  HTTP   │    (Python)      │  API    │  OpenAI/Claude  │
│                 │◀────────│                  │◀────────│                 │
└─────────────────┘  JSON   └──────────────────┘  JSON   └─────────────────┘
        │                            │
        │                            │
        ▼                            ▼
   Tailwind CSS              PDF Extraction
   React Query                 (PyPDF2)
   Axios
```

### Clean Architecture Layers

**Backend:**
```
app/
├── api/           # API routes (presentation layer)
├── services/      # Business logic
├── schemas/       # Data validation
├── core/          # Configuration
└── utils/         # Utilities
```

**Frontend:**
```
src/
├── components/    # UI components
├── pages/         # Page components
├── hooks/         # Custom React hooks
├── services/      # API client
└── types/         # TypeScript types
```

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **PyPDF2** - PDF text extraction
- **OpenAI / Anthropic** - AI analysis
- **Uvicorn** - ASGI server
- **Python 3.11+**

### Frontend
- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Utility-first CSS
- **React Query** - Data fetching & caching
- **Axios** - HTTP client
- **React Hot Toast** - Notifications

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Production web server

---

## 🚀 Getting Started

### Prerequisites

- **Docker & Docker Compose** (recommended)
  - OR -
- **Python 3.11+** and **Node.js 20+**

### Quick Start with Docker (Recommended)

1. **Clone the repository**
   ```bash
   cd "c:\Users\PC\Desktop\Nouveau dossier"
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and set AI_PROVIDER (mock, openai, or anthropic)
   # For openai/anthropic, add your AI_API_KEY
   ```

3. **Start services**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/api/docs

### Local Development Setup

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run development server
uvicorn app.main:app --reload
```

Backend runs at: http://localhost:8000

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env

# Run development server
npm run dev
```

Frontend runs at: http://localhost:5173

---

## 📚 API Documentation

### Endpoints

#### `GET /`
Health check endpoint
```json
{
  "status": "healthy",
  "service": "SmartResume Analyzer",
  "version": "1.0.0"
}
```

#### `GET /health`
Detailed health check
```json
{
  "status": "healthy",
  "checks": {
    "api": "operational",
    "ai_service": "configured"
  }
}
```

#### `POST /api/analyze`
Analyze CV against job description

**Request:**
- Content-Type: `multipart/form-data`
- `cv_file`: PDF file (max 10MB)
- `job_description`: Text (10-5000 characters)

**Response:**
```json
{
  "score": 85.5,
  "matching_skills": ["Python", "FastAPI", "Docker", "React"],
  "missing_skills": ["Kubernetes", "AWS"],
  "strengths": [
    "Strong backend development experience",
    "Modern tech stack proficiency"
  ],
  "areas_for_improvement": [
    "Could benefit from cloud certifications",
    "Leadership experience could be highlighted more"
  ],
  "recommendation": "The candidate shows an 85.5% match with the job requirements..."
}
```

**Error Response:**
```json
{
  "detail": "Error message here"
}
```

### Interactive API Documentation

- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

---

## 📁 Project Structure

```
smartresume-analyzer/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── analyze.py          # Analysis endpoint
│   │   ├── services/
│   │   │   ├── ai_service.py       # AI integration layer
│   │   │   └── pdf_service.py      # PDF text extraction
│   │   ├── schemas/
│   │   │   └── analysis.py         # Pydantic models
│   │   ├── core/
│   │   │   └── config.py           # Configuration management
│   │   ├── utils/
│   │   │   └── logger.py           # Logging setup
│   │   └── main.py                 # FastAPI application
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FileUpload.tsx      # File upload component
│   │   │   ├── JobDescriptionInput.tsx
│   │   │   └── ResultCard.tsx      # Results display
│   │   ├── hooks/
│   │   │   └── useAnalyzeCV.ts     # React Query hook
│   │   ├── pages/
│   │   │   └── Home.tsx            # Main page
│   │   ├── services/
│   │   │   └── api.ts              # API client
│   │   ├── types/
│   │   │   └── analysis.ts         # TypeScript types
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   └── vite.config.ts
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

---

## 💻 Development

### Code Quality Principles

This project demonstrates:

- ✅ **Clean Code** - Readable, maintainable, well-commented code
- ✅ **SOLID Principles** - Single responsibility, dependency injection
- ✅ **Separation of Concerns** - Clear layer boundaries
- ✅ **Type Safety** - Pydantic (Python) and TypeScript
- ✅ **Error Handling** - Comprehensive error handling
- ✅ **Logging** - Structured logging throughout
- ✅ **Configuration Management** - Environment-based config
- ✅ **API Documentation** - Auto-generated OpenAPI docs

### Backend Development

```bash
cd backend

# Install dev dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest

# Run with auto-reload
uvicorn app.main:app --reload --log-level debug
```

### Frontend Development

```bash
cd frontend

# Run dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Type checking
npm run lint
```

---

## 🚢 Deployment

### Docker Deployment (Production)

```bash
# Build images
docker-compose build

# Run in production mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Cloud Deployment Options

#### AWS (ECS + ECR)
1. Push Docker images to ECR
2. Create ECS task definitions
3. Deploy to ECS Fargate or EC2
4. Configure ALB for load balancing

#### Railway / Render
1. Connect GitHub repository
2. Configure build settings
3. Set environment variables
4. Deploy automatically on push

#### DigitalOcean App Platform
1. Import from GitHub
2. Configure services (backend + frontend)
3. Set environment variables
4. Deploy

---

## ⚙️ Configuration

### Backend Environment Variables

```bash
# Application
APP_NAME=SmartResume Analyzer
ENVIRONMENT=development  # or production
DEBUG=True

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# AI Provider
AI_PROVIDER=mock  # mock, openai, or anthropic
AI_API_KEY=your-api-key-here
AI_MODEL=gpt-4  # or claude-3-5-sonnet-20241022
AI_MAX_TOKENS=1000
AI_TEMPERATURE=0.3

# File Upload
MAX_FILE_SIZE_MB=10
ALLOWED_EXTENSIONS=pdf

# Logging
LOG_LEVEL=INFO
```

### Frontend Environment Variables

```bash
VITE_API_URL=http://localhost:8000
```

### AI Provider Setup

**Using OpenAI:**
```bash
AI_PROVIDER=openai
AI_API_KEY=sk-...
AI_MODEL=gpt-4
```

**Using Anthropic:**
```bash
AI_PROVIDER=anthropic
AI_API_KEY=sk-ant-...
AI_MODEL=claude-3-5-sonnet-20241022
```

**Using Mock (no API key needed):**
```bash
AI_PROVIDER=mock
```

---

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest

# With coverage
pytest --cov=app --cov-report=html
```

### Frontend Tests

```bash
cd frontend
npm test

# With coverage
npm test -- --coverage
```

---

## 🤝 Contributing

This is a demo project for learning purposes. Feel free to:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

MIT License - feel free to use this project for learning and demonstration purposes.

---

## 🎓 Learning Objectives

This project demonstrates:

- Full-stack development with modern frameworks
- Clean architecture and code principles
- RESTful API design
- AI/LLM integration with abstraction
- Docker containerization
- React best practices
- TypeScript type safety
- State management with React Query
- File upload handling
- Error handling and validation
- Production-ready deployment

---

## 👨‍💻 Author

Built as a technical demonstration project showcasing clean architecture and full-stack development best practices.

---

## 🙏 Acknowledgments

- FastAPI for excellent Python web framework
- React team for amazing frontend library
- OpenAI and Anthropic for AI capabilities
- Tailwind CSS for beautiful styling utilities

---

**Happy Coding! 🚀**
