"""
CV Analysis API Endpoint
Handles CV upload and analysis requests
"""

from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from fastapi.responses import JSONResponse
from app.schemas.analysis import AnalysisResponse, ErrorResponse
from app.services.pdf_service import pdf_service
from app.services.ai_service import ai_service
from app.core.config import settings
from app.utils.logger import logger


router = APIRouter()


@router.post(
    "/analyze",
    response_model=AnalysisResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    },
    summary="Analyze CV against job description",
    description="Upload a CV (PDF) and provide a job description to get an AI-powered match analysis"
)
async def analyze_cv(
    cv_file: UploadFile = File(..., description="CV file in PDF format"),
    job_description: str = Form(..., description="Job description text")
):
    """
    Analyze a CV against a job description and return structured feedback
    
    The endpoint:
    1. Validates the uploaded PDF file
    2. Extracts text from the PDF
    3. Sends CV text and job description to AI service
    4. Returns structured analysis with score, matching/missing skills, and recommendations
    """
    
    # Validate file type
    if not cv_file.filename.lower().endswith('.pdf'):
        logger.warning(f"Invalid file type uploaded: {cv_file.filename}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are supported"
        )
    
    # Validate job description
    if not job_description or len(job_description.strip()) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Job description must be at least 10 characters"
        )
    
    try:
        # Read file content
        cv_content = await cv_file.read()
        
        # Check file size
        file_size_mb = len(cv_content) / (1024 * 1024)
        if file_size_mb > settings.MAX_FILE_SIZE_MB:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File size exceeds maximum limit of {settings.MAX_FILE_SIZE_MB}MB"
            )
        
        logger.info(f"Processing CV: {cv_file.filename} ({file_size_mb:.2f}MB)")
        
        # Validate PDF
        if not pdf_service.validate_pdf(cv_content):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or corrupted PDF file"
            )
        
        # Extract text from PDF
        try:
            cv_text = pdf_service.extract_text_from_pdf(cv_content)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )
        
        # Analyze CV with AI
        try:
            analysis_result = await ai_service.analyze_resume(cv_text, job_description)
        except Exception as e:
            logger.error(f"AI analysis error: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Analysis failed: {str(e)}"
            )
        
        logger.info(f"Successfully analyzed CV with score: {analysis_result.get('score', 0)}")
        
        return AnalysisResponse(**analysis_result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in analyze_cv: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}"
        )
