# SmartResume Analyzer - Architecture Diagram

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            USER INTERFACE                                    │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                      React Frontend (Port 3000/5173)                │    │
│  │                                                                     │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │    │
│  │  │  FileUpload  │  │ JobDescInput │  │  ResultCard  │            │    │
│  │  │  Component   │  │  Component   │  │  Component   │            │    │
│  │  └──────────────┘  └──────────────┘  └──────────────┘            │    │
│  │                            │                                       │    │
│  │                            ▼                                       │    │
│  │                   ┌─────────────────┐                             │    │
│  │                   │  Home Page      │                             │    │
│  │                   └─────────────────┘                             │    │
│  │                            │                                       │    │
│  │                            ▼                                       │    │
│  │                   ┌─────────────────┐                             │    │
│  │                   │ useAnalyzeCV    │ (React Query Hook)          │    │
│  │                   │ Hook            │                             │    │
│  │                   └─────────────────┘                             │    │
│  │                            │                                       │    │
│  │                            ▼                                       │    │
│  │                   ┌─────────────────┐                             │    │
│  │                   │  API Service    │ (Axios)                     │    │
│  │                   └─────────────────┘                             │    │
│  └────────────────────────────┬────────────────────────────────────┘    │
└────────────────────────────────┼─────────────────────────────────────────┘
                                 │
                                 │ HTTP/JSON
                                 │ POST /api/analyze
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         BACKEND API (Port 8000)                              │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │                       FastAPI Application                           │    │
│  │                                                                     │    │
│  │  ┌──────────────────────────────────────────────────────────────┐ │    │
│  │  │                      API Layer                                │ │    │
│  │  │  ┌────────────────┐                                          │ │    │
│  │  │  │ analyze.py     │  POST /api/analyze                       │ │    │
│  │  │  │ (Router)       │  - File upload handling                  │ │    │
│  │  │  │                │  - Request validation                    │ │    │
│  │  │  │                │  - Response formatting                   │ │    │
│  │  │  └────────┬───────┘                                          │ │    │
│  │  └───────────┼──────────────────────────────────────────────────┘ │    │
│  │              │                                                     │    │
│  │              ▼                                                     │    │
│  │  ┌──────────────────────────────────────────────────────────────┐ │    │
│  │  │                    Services Layer                             │ │    │
│  │  │                                                               │ │    │
│  │  │  ┌────────────────┐              ┌────────────────┐          │ │    │
│  │  │  │ pdf_service.py │              │ ai_service.py  │          │ │    │
│  │  │  │                │              │                │          │ │    │
│  │  │  │ - Extract text │              │ - AI Provider  │          │ │    │
│  │  │  │   from PDF     │              │   Abstraction  │          │ │    │
│  │  │  │ - Validate PDF │              │ - OpenAI       │          │ │    │
│  │  │  │                │              │ - Anthropic    │          │ │    │
│  │  │  │                │              │ - Mock         │          │ │    │
│  │  │  └────────────────┘              └────────┬───────┘          │ │    │
│  │  └───────────────────────────────────────────┼──────────────────┘ │    │
│  │                                               │                    │    │
│  │  ┌──────────────────────────────────────────┼──────────────────┐ │    │
│  │  │                    Schemas Layer          │                  │ │    │
│  │  │  ┌────────────────────────────────────────▼───────────────┐ │ │    │
│  │  │  │ analysis.py (Pydantic)                                 │ │ │    │
│  │  │  │ - AnalysisRequest   (validation)                       │ │ │    │
│  │  │  │ - AnalysisResponse  (serialization)                    │ │ │    │
│  │  │  │ - ErrorResponse                                        │ │ │    │
│  │  │  └────────────────────────────────────────────────────────┘ │ │    │
│  │  └────────────────────────────────────────────────────────────┘ │    │
│  │                                                                  │    │
│  │  ┌──────────────────────────────────────────────────────────────┐ │    │
│  │  │                      Core & Utils                             │ │    │
│  │  │  ┌────────────────┐              ┌────────────────┐          │ │    │
│  │  │  │ config.py      │              │ logger.py      │          │ │    │
│  │  │  │ - Settings     │              │ - Logging      │          │ │    │
│  │  │  │ - Environment  │              │ - Structured   │          │ │    │
│  │  │  └────────────────┘              └────────────────┘          │ │    │
│  │  └──────────────────────────────────────────────────────────────┘ │    │
│  └────────────────────────────────────────────────────────────────────┘    │
└────────────────────────────────┬─────────────────────────────────────────────┘
                                 │
                                 │ API Calls
                                 │ (OpenAI/Anthropic SDK)
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                          EXTERNAL SERVICES                                   │
│                                                                              │
│  ┌────────────────┐      ┌────────────────┐      ┌────────────────┐        │
│  │   OpenAI API   │      │ Anthropic API  │      │   Mock AI      │        │
│  │   (GPT-4)      │      │   (Claude)     │      │   (Testing)    │        │
│  └────────────────┘      └────────────────┘      └────────────────┘        │
└──────────────────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
1. USER UPLOADS CV & ENTERS JOB DESCRIPTION
   │
   ├─► FileUpload component handles CV file
   └─► JobDescriptionInput component handles job description
        │
        ▼
2. FORM SUBMISSION
   │
   └─► Home page validates inputs
        │
        ▼
3. API CALL VIA REACT QUERY
   │
   └─► useAnalyzeCV hook triggered
        │
        └─► api.ts makes HTTP request
             │
             ▼
4. BACKEND RECEIVES REQUEST
   │
   └─► analyze.py endpoint
        │
        ├─► Validates file type (PDF only)
        ├─► Validates file size (< 10MB)
        └─► Validates job description (10-5000 chars)
             │
             ▼
5. PDF TEXT EXTRACTION
   │
   └─► pdf_service.py
        │
        ├─► Reads PDF bytes
        ├─► Extracts text from all pages
        └─► Returns combined text
             │
             ▼
6. AI ANALYSIS
   │
   └─► ai_service.py
        │
        ├─► Selects provider (OpenAI/Anthropic/Mock)
        ├─► Constructs prompt
        ├─► Calls AI API
        └─► Parses JSON response
             │
             ▼
7. RESPONSE VALIDATION
   │
   └─► Pydantic schema validates response structure
        │
        └─► Ensures all required fields present
             │
             ▼
8. RETURN TO FRONTEND
   │
   └─► FastAPI serializes to JSON
        │
        └─► CORS headers added
             │
             ▼
9. FRONTEND RECEIVES DATA
   │
   └─► React Query caches result
        │
        └─► ResultCard component displays analysis
             │
             ▼
10. USER VIEWS RESULTS
    │
    ├─► Match score
    ├─► Matching skills
    ├─► Missing skills
    ├─► Strengths
    ├─► Areas for improvement
    └─► Detailed recommendation
```

## Technology Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                        FRONTEND STACK                            │
├─────────────────────────────────────────────────────────────────┤
│  React 18          │  UI Library                                │
│  TypeScript        │  Type Safety                               │
│  Vite              │  Build Tool & Dev Server                   │
│  Tailwind CSS      │  Styling                                   │
│  React Query       │  Server State Management                   │
│  Axios             │  HTTP Client                               │
│  React Hot Toast   │  Notifications                             │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                        BACKEND STACK                             │
├─────────────────────────────────────────────────────────────────┤
│  FastAPI           │  Web Framework                             │
│  Pydantic          │  Data Validation                           │
│  PyPDF2            │  PDF Text Extraction                       │
│  OpenAI SDK        │  GPT-4 Integration (optional)              │
│  Anthropic SDK     │  Claude Integration (optional)             │
│  Uvicorn           │  ASGI Server                               │
│  Python 3.11+      │  Programming Language                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                         DEVOPS STACK                             │
├─────────────────────────────────────────────────────────────────┤
│  Docker            │  Containerization                          │
│  Docker Compose    │  Multi-Container Orchestration             │
│  Nginx             │  Reverse Proxy & Static File Server        │
└─────────────────────────────────────────────────────────────────┘
```

## Deployment Architecture

```
                              PRODUCTION DEPLOYMENT

┌────────────────────────────────────────────────────────────────────────────┐
│                               CLOUD PROVIDER                                │
│                         (AWS / Railway / Render / DO)                       │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │                         Load Balancer / CDN                           │ │
│  │                            (HTTPS/SSL)                                │ │
│  └──────────────────────┬───────────────────────────────────────────────┘ │
│                         │                                                  │
│         ┌───────────────┴──────────────┐                                  │
│         │                               │                                  │
│         ▼                               ▼                                  │
│  ┌──────────────┐              ┌──────────────┐                           │
│  │   Frontend   │              │   Backend    │                           │
│  │  Container   │              │  Container   │                           │
│  │              │              │              │                           │
│  │  Nginx:80    │              │  Uvicorn:8000│                           │
│  │  React App   │◄────────────►│  FastAPI App │                           │
│  │              │   API Proxy  │              │                           │
│  └──────────────┘              └──────┬───────┘                           │
│                                       │                                    │
│                                       │ API Calls                          │
│                                       ▼                                    │
│                              ┌─────────────────┐                           │
│                              │  External APIs  │                           │
│                              │  OpenAI/Claude  │                           │
│                              └─────────────────┘                           │
└────────────────────────────────────────────────────────────────────────────┘
```

## Security Architecture

```
┌────────────────────────────────────────────────────────────────────────────┐
│                           SECURITY LAYERS                                   │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. NETWORK LAYER                                                          │
│     ├─ HTTPS/TLS encryption                                               │
│     ├─ CORS policy enforcement                                            │
│     └─ Rate limiting (future)                                             │
│                                                                             │
│  2. APPLICATION LAYER                                                      │
│     ├─ Input validation (Pydantic)                                        │
│     ├─ File type validation (PDF only)                                    │
│     ├─ File size limits (10MB max)                                        │
│     ├─ Error handling (no info leakage)                                   │
│     └─ Sanitized logging                                                  │
│                                                                             │
│  3. INFRASTRUCTURE LAYER                                                   │
│     ├─ Docker container isolation                                         │
│     ├─ Environment variable secrets                                       │
│     ├─ Non-root user in containers                                        │
│     └─ Security headers (X-Frame-Options, etc.)                           │
│                                                                             │
│  4. DATA LAYER                                                             │
│     ├─ No sensitive data persistence                                      │
│     ├─ Temporary file handling                                            │
│     └─ API key encryption in transit                                      │
└────────────────────────────────────────────────────────────────────────────┘
```

---

This architecture demonstrates:
- ✅ Clean separation of concerns
- ✅ Scalable component design
- ✅ Production-ready infrastructure
- ✅ Security best practices
- ✅ Modern tech stack integration
