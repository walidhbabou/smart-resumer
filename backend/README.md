# SmartResume Analyzer - Backend

FastAPI backend for AI-powered CV analysis.

## Setup

### Local Development

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your settings
```

4. Run server:
```bash
uvicorn app.main:app --reload
```

Server runs at: http://localhost:8000
API docs: http://localhost:8000/api/docs

### Docker

```bash
docker build -t smartresume-backend .
docker run -p 8000:8000 --env-file .env smartresume-backend
```

## API Endpoints

### POST /api/analyze
Analyze CV against job description

**Request:**
- `cv_file`: PDF file (multipart/form-data)
- `job_description`: Job description text (form field)

**Response:**
```json
{
  "score": 85.5,
  "matching_skills": ["Python", "FastAPI", "Docker"],
  "missing_skills": ["Kubernetes", "AWS"],
  "strengths": ["Strong backend experience"],
  "areas_for_improvement": ["Cloud certifications"],
  "recommendation": "Strong candidate with relevant skills..."
}
```

## Configuration

Edit `.env` file:

- `AI_PROVIDER`: Choose `openai`, `anthropic`, or `mock`
- `AI_API_KEY`: Your API key
- `AI_MODEL`: Model name (e.g., `gpt-4`, `claude-3-5-sonnet-20241022`)

## Testing

```bash
pytest
```
