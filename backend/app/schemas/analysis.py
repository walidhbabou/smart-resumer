"""
Pydantic Schemas for CV Analysis
Data validation and serialization models
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
    """Request schema for CV analysis"""
    job_description: str = Field(
        ..., 
        description="Job description to match against the CV",
        min_length=10,
        max_length=5000
    )


class AnalysisResponse(BaseModel):
    """Response schema for CV analysis results"""
    score: float = Field(
        ..., 
        description="Match score between 0 and 100",
        ge=0,
        le=100
    )
    matching_skills: List[str] = Field(
        default_factory=list,
        description="Skills from CV that match the job requirements"
    )
    missing_skills: List[str] = Field(
        default_factory=list,
        description="Important skills mentioned in job description but missing from CV"
    )
    recommendation: str = Field(
        ...,
        description="Detailed recommendation and analysis summary"
    )
    strengths: Optional[List[str]] = Field(
        default_factory=list,
        description="Key strengths identified in the CV"
    )
    areas_for_improvement: Optional[List[str]] = Field(
        default_factory=list,
        description="Areas where the candidate could improve"
    )


class ErrorResponse(BaseModel):
    """Error response schema"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
