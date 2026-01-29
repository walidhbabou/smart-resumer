/**
 * Analysis Types
 * TypeScript interfaces matching the backend API schema
 */

export interface AnalysisRequest {
  cv_file: File;
  job_description: string;
}

export interface AnalysisResponse {
  score: number;
  matching_skills: string[];
  missing_skills: string[];
  recommendation: string;
  strengths?: string[];
  areas_for_improvement?: string[];
}

export interface ErrorResponse {
  error: string;
  detail?: string;
}
