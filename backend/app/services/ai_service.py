"""
AI Service
Abstraction layer for LLM integration (OpenAI, Anthropic, or Mock)
"""

import json
from typing import Dict, Any
from abc import ABC, abstractmethod
from app.core.config import settings
from app.utils.logger import logger


class BaseAIProvider(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    async def analyze_cv(self, cv_text: str, job_description: str) -> Dict[str, Any]:
        """Analyze CV against job description"""
        pass


class OpenAIProvider(BaseAIProvider):
    """OpenAI GPT-4 implementation"""
    
    def __init__(self):
        try:
            import openai
            self.client = openai.OpenAI(api_key=settings.AI_API_KEY)
            logger.info("OpenAI provider initialized")
        except ImportError:
            raise ImportError("openai package not installed. Run: pip install openai")
    
    async def analyze_cv(self, cv_text: str, job_description: str) -> Dict[str, Any]:
        """Analyze CV using OpenAI GPT-4"""
        prompt = self._create_analysis_prompt(cv_text, job_description)
        
        try:
            response = self.client.chat.completions.create(
                model=settings.AI_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert HR consultant and career advisor. Analyze CVs against job descriptions and provide structured feedback in JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=settings.AI_TEMPERATURE,
                max_tokens=settings.AI_MAX_TOKENS,
                response_format={"type": "json_object"}
            )
            
            result = json.loads(response.choices[0].message.content)
            logger.info("Successfully analyzed CV with OpenAI")
            return result
            
        except Exception as e:
            logger.error(f"OpenAI analysis failed: {str(e)}")
            raise
    
    def _create_analysis_prompt(self, cv_text: str, job_description: str) -> str:
        """Create structured prompt for CV analysis"""
        return f"""
Analyze the following CV against the job description and provide a detailed assessment.

JOB DESCRIPTION:
{job_description}

CANDIDATE CV:
{cv_text}

Provide your analysis in the following JSON format:
{{
    "score": <number between 0-100 indicating match quality>,
    "matching_skills": [<list of skills from CV that match job requirements>],
    "missing_skills": [<list of important skills from job description missing in CV>],
    "strengths": [<list of candidate's key strengths>],
    "areas_for_improvement": [<list of areas where candidate could improve>],
    "recommendation": "<detailed text recommendation explaining the match, strengths, gaps, and overall assessment>"
}}

Be specific, actionable, and constructive in your analysis.
"""


class AnthropicProvider(BaseAIProvider):
    """Anthropic Claude implementation"""
    
    def __init__(self):
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=settings.AI_API_KEY)
            logger.info("Anthropic provider initialized")
        except ImportError:
            raise ImportError("anthropic package not installed. Run: pip install anthropic")
    
    async def analyze_cv(self, cv_text: str, job_description: str) -> Dict[str, Any]:
        """Analyze CV using Anthropic Claude"""
        prompt = self._create_analysis_prompt(cv_text, job_description)
        
        try:
            response = self.client.messages.create(
                model=settings.AI_MODEL or "claude-3-5-sonnet-20241022",
                max_tokens=settings.AI_MAX_TOKENS,
                temperature=settings.AI_TEMPERATURE,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            # Extract JSON from response
            content = response.content[0].text
            # Try to find JSON in the response
            start_idx = content.find('{')
            end_idx = content.rfind('}') + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = content[start_idx:end_idx]
                result = json.loads(json_str)
            else:
                result = json.loads(content)
            
            logger.info("Successfully analyzed CV with Anthropic")
            return result
            
        except Exception as e:
            logger.error(f"Anthropic analysis failed: {str(e)}")
            raise
    
    def _create_analysis_prompt(self, cv_text: str, job_description: str) -> str:
        """Create structured prompt for CV analysis"""
        return f"""
Analyze the following CV against the job description and provide a detailed assessment.

JOB DESCRIPTION:
{job_description}

CANDIDATE CV:
{cv_text}

Provide your analysis in the following JSON format:
{{
    "score": <number between 0-100 indicating match quality>,
    "matching_skills": [<list of skills from CV that match job requirements>],
    "missing_skills": [<list of important skills from job description missing in CV>],
    "strengths": [<list of candidate's key strengths>],
    "areas_for_improvement": [<list of areas where candidate could improve>],
    "recommendation": "<detailed text recommendation explaining the match, strengths, gaps, and overall assessment>"
}}

Be specific, actionable, and constructive in your analysis. Return ONLY valid JSON.
"""


class GeminiProvider(BaseAIProvider):
    """Google Gemini implementation"""
    
    def __init__(self):
        try:
            from google import genai
            from google.genai import types
            self.client = genai.Client(api_key=settings.AI_API_KEY)
            self.types = types  # Store types for use in methods
            # Use Gemini 2.5 models (current generation)
            self.model_name = settings.AI_MODEL or 'gemini-2.5-flash'
            logger.info(f"Gemini provider initialized with model: {self.model_name}")
        except ImportError:
            raise ImportError("google-genai package not installed. Run: pip install google-genai")
    
    async def analyze_cv(self, cv_text: str, job_description: str) -> Dict[str, Any]:
        """Analyze CV using Google Gemini"""
        prompt = self._create_analysis_prompt(cv_text, job_description)
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=self.types.GenerateContentConfig(
                    temperature=settings.AI_TEMPERATURE,
                    max_output_tokens=8192,  # Increased for complete response
                    response_mime_type="application/json",  # Force JSON response
                )
            )
            
            # Extract full content from response
            if hasattr(response, 'text'):
                content = response.text.strip()
            elif hasattr(response, 'candidates') and len(response.candidates) > 0:
                content = response.candidates[0].content.parts[0].text.strip()
            else:
                content = str(response).strip()
            
            # Log the raw response for debugging
            logger.info(f"Raw Gemini response length: {len(content)} chars")
            logger.debug(f"Raw Gemini response: {content[:500]}")
            
            # Try to parse JSON directly first
            try:
                result = json.loads(content)
            except json.JSONDecodeError:
                # If direct parsing fails, try to extract JSON from markdown code blocks
                if "```json" in content:
                    start_idx = content.find("```json") + 7
                    end_idx = content.find("```", start_idx)
                    json_str = content[start_idx:end_idx].strip()
                    result = json.loads(json_str)
                elif "```" in content:
                    start_idx = content.find("```") + 3
                    end_idx = content.find("```", start_idx)
                    json_str = content[start_idx:end_idx].strip()
                    result = json.loads(json_str)
                else:
                    # Try to find JSON object in the response
                    start_idx = content.find('{')
                    end_idx = content.rfind('}') + 1
                    if start_idx != -1 and end_idx > start_idx:
                        json_str = content[start_idx:end_idx]
                        result = json.loads(json_str)
                    else:
                        raise ValueError(f"Could not extract valid JSON from response: {content[:200]}")
            
            logger.info("Successfully analyzed CV with Gemini")
            return result
            
        except Exception as e:
            logger.error(f"Gemini analysis failed: {str(e)}")
            raise
    
    def _create_analysis_prompt(self, cv_text: str, job_description: str) -> str:
        """Create structured prompt for CV analysis"""
        return f"""
You are an expert HR consultant and career advisor. Analyze the following CV against the job description and provide a detailed assessment.

JOB DESCRIPTION:
{job_description}

CANDIDATE CV:
{cv_text}

Provide your analysis in the following JSON format (return ONLY valid JSON, no additional text):
{{
    "score": <number between 0-100 indicating match quality>,
    "matching_skills": [<list of skills from CV that match job requirements>],
    "missing_skills": [<list of important skills from job description missing in CV>],
    "strengths": [<list of candidate's key strengths>],
    "areas_for_improvement": [<list of areas where candidate could improve>],
    "recommendation": "<detailed text recommendation explaining the match, strengths, gaps, and overall assessment>"
}}

Be specific, actionable, and constructive in your analysis. Return ONLY valid JSON.
"""


class MockAIProvider(BaseAIProvider):
    """Mock provider for testing without API keys"""
    
    def __init__(self):
        logger.info("Mock AI provider initialized (for testing)")
    
    async def analyze_cv(self, cv_text: str, job_description: str) -> Dict[str, Any]:
        """Return mock analysis data"""
        logger.info("Generating mock CV analysis")
        
        # Simple keyword matching for demo
        cv_lower = cv_text.lower()
        jd_lower = job_description.lower()
        
        # Extract some keywords for matching
        common_skills = ["python", "javascript", "react", "fastapi", "docker", "aws", 
                        "sql", "git", "api", "testing", "agile", "typescript"]
        
        matching = [skill for skill in common_skills if skill in cv_lower and skill in jd_lower]
        missing = [skill for skill in common_skills if skill in jd_lower and skill not in cv_lower]
        
        score = min(100, (len(matching) / max(1, len(matching) + len(missing))) * 100 + 20)
        
        return {
            "score": round(score, 1),
            "matching_skills": matching[:5] if matching else ["Communication", "Problem Solving"],
            "missing_skills": missing[:5] if missing else ["Leadership", "Project Management"],
            "strengths": [
                "Strong technical background",
                "Relevant work experience",
                "Clear communication skills"
            ],
            "areas_for_improvement": [
                "Could highlight more specific achievements",
                "Consider adding certifications",
                "Expand on leadership experience"
            ],
            "recommendation": f"The candidate shows a {score:.0f}% match with the job requirements. "
                            f"They demonstrate strong skills in {', '.join(matching[:3]) if matching else 'core competencies'}. "
                            f"To improve their profile, they should focus on developing {', '.join(missing[:2]) if missing else 'additional skills'}. "
                            f"Overall, this is a {'strong' if score > 70 else 'moderate' if score > 50 else 'developing'} candidate for the role."
        }


class AIService:
    """Main AI service that routes to appropriate provider"""
    
    def __init__(self):
        self.provider = self._initialize_provider()
    
    def _initialize_provider(self) -> BaseAIProvider:
        """Initialize the appropriate AI provider based on configuration"""
        provider_name = settings.AI_PROVIDER.lower()
        
        if provider_name == "openai":
            if not settings.AI_API_KEY:
                logger.warning("No API key provided, falling back to mock provider")
                return MockAIProvider()
            return OpenAIProvider()
        
        elif provider_name == "anthropic":
            if not settings.AI_API_KEY:
                logger.warning("No API key provided, falling back to mock provider")
                return MockAIProvider()
            return AnthropicProvider()
        
        elif provider_name == "gemini":
            if not settings.AI_API_KEY:
                logger.warning("No API key provided, falling back to mock provider")
                return MockAIProvider()
            return GeminiProvider()
        
        elif provider_name == "mock":
            return MockAIProvider()
        
        else:
            logger.warning(f"Unknown provider '{provider_name}', using mock")
            return MockAIProvider()
    
    async def analyze_resume(self, cv_text: str, job_description: str) -> Dict[str, Any]:
        """
        Analyze resume against job description
        
        Args:
            cv_text: Extracted text from CV
            job_description: Job description text
            
        Returns:
            Analysis results dictionary
        """
        logger.info(f"Starting CV analysis using {self.provider.__class__.__name__}")
        
        try:
            result = await self.provider.analyze_cv(cv_text, job_description)
            
            # Ensure all required fields are present
            required_fields = ["score", "matching_skills", "missing_skills", "recommendation"]
            for field in required_fields:
                if field not in result:
                    raise ValueError(f"Missing required field: {field}")
            
            return result
            
        except Exception as e:
            logger.error(f"CV analysis failed: {str(e)}")
            raise


# Create global instance
ai_service = AIService()
